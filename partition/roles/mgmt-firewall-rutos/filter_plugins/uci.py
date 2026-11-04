from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
import shlex

from ansible.errors import AnsibleFilterError

NAME = re.compile(r"^[A-Za-z0-9_]+$")
TYPE = re.compile(r"^[A-Za-z0-9_-]+$")
INDEXED = re.compile(r"^@([A-Za-z0-9_-]+)\[(\d+|\*)\]$")


def uci_parse_export(text):
    packages = {}
    sections = None
    for line in text.splitlines():
        words = shlex.split(line.strip())
        if not words:
            continue
        keyword = words[0]
        if keyword == "package":
            sections = packages.setdefault(words[1], [])
        elif keyword == "config":
            sections.append(new_section(sections, words[1], words[2] if len(words) > 2 else None))
        elif keyword == "option":
            sections[-1]["options"][words[1]] = words[2] if len(words) > 2 else ""
        elif keyword == "list":
            sections[-1]["options"].setdefault(words[1], []).append(words[2] if len(words) > 2 else "")
    return packages


def new_section(sections, section_type, name):
    index = sum(1 for s in sections if s["type"] == section_type)
    return dict(type=section_type, name=name, index=index, options={})


def uci_batch(export_text, desired):
    current = uci_parse_export(export_text)
    batch = []
    for package, spec in desired.items():
        require_name(package, "package")
        if package not in current:
            raise AnsibleFilterError("package %s was not exported from the device, add it to the export list or remove it from the desired state" % package)
        batch.extend(package_batch(package, current[package], spec or {}))
    return batch


def uci_batch_packages(batch):
    packages = []
    for command in batch:
        package = command.split(" ", 1)[1].split(".", 1)[0].split("=", 1)[0]
        if package not in packages:
            packages.append(package)
    return packages


def uci_batch_chunks(batch, max_bytes):
    chunks = []
    current = []
    size = 0
    for command in batch:
        length = len(command) + 1
        if length > max_bytes:
            raise AnsibleFilterError("uci command is longer than %d bytes, raise mgmt_firewall_rutos_chunk_bytes: %s" % (max_bytes, command))
        if current and size + length > max_bytes:
            chunks.append(current)
            current = []
            size = 0
        current.append(command)
        size += length
    if current:
        chunks.append(current)
    return chunks


def package_batch(package, sections, spec):
    purge = list(spec.get("purge", []))
    purge_anonymous = list(spec.get("purge_anonymous", []))
    declared = spec.get("sections", {}) or {}
    require_indexed_types_are_stable(package, declared, purge + purge_anonymous)
    batch = purge_batch(package, sections, purge, purge_anonymous, declared)
    for key, section_spec in declared.items():
        section_spec = section_spec or {}
        match = INDEXED.match(key)
        if match:
            batch.extend(indexed_batch(package, sections, match.group(1), match.group(2), section_spec))
        else:
            batch.extend(named_batch(package, sections, key, section_spec))
    return batch


def require_indexed_types_are_stable(package, declared, purge):
    named_types = {spec.get("type") for key, spec in declared.items() if not INDEXED.match(key) and spec}
    for key in declared:
        match = INDEXED.match(key)
        if match and (match.group(1) in purge or match.group(1) in named_types):
            raise AnsibleFilterError(
                "%s.%s addresses a section by index while sections of type %s are deleted or created in the same run, "
                "declare it by name instead" % (package, key, match.group(1))
            )


def purge_batch(package, sections, purge, purge_anonymous, declared):
    doomed = [
        s for s in sections
        if (s["type"] in purge and s["name"] not in declared) or (s["type"] in purge_anonymous and s["name"] is None)
    ]
    doomed.sort(key=lambda s: s["index"], reverse=True)
    return ["delete %s" % address(package, s) for s in doomed]


def indexed_batch(package, sections, section_type, index, spec):
    matching = [s for s in sections if s["type"] == section_type]
    if index != "*":
        matching = [s for s in matching if s["index"] == int(index)]
        if not matching:
            raise AnsibleFilterError(
                "%s.@%s[%s] does not exist on the device, check the index or declare the section by name" % (package, section_type, index)
            )
    batch = []
    for section in matching:
        batch.extend(options_batch(address(package, section), section["options"], spec.get("options", {}), exclusive=False))
    return batch


def named_batch(package, sections, name, spec):
    require_name(name, "section")
    section_type = spec.get("type")
    if not section_type:
        raise AnsibleFilterError("%s.%s has no type, set type to the uci section type" % (package, name))
    require_type(section_type)
    existing = next((s for s in sections if s["name"] == name), None)
    target = "%s.%s" % (package, name)
    batch = []
    current_options = {}
    if existing and existing["type"] != section_type:
        batch.append("delete %s" % target)
        existing = None
    if existing:
        current_options = existing["options"]
    else:
        batch.append("set %s=%s" % (target, section_type))
    exclusive = not spec.get("merge", False)
    batch.extend(options_batch(target, current_options, spec.get("options", {}), exclusive))
    return batch


def options_batch(target, current, desired, exclusive):
    batch = []
    for option, value in (desired or {}).items():
        require_name(option, "option")
        batch.extend(option_batch("%s.%s" % (target, option), option in current, current.get(option), uci_value(value)))
    if exclusive:
        batch.extend("delete %s.%s" % (target, option) for option in current if option not in (desired or {}))
    return batch


def option_batch(path, present, current, value):
    if value is None:
        return ["delete %s" % path] if present else []
    if value == current:
        return []
    batch = ["delete %s" % path] if present and (isinstance(value, list) or isinstance(current, list)) else []
    if isinstance(value, list):
        batch.extend("add_list %s=%s" % (path, quote(item)) for item in value)
    else:
        batch.append("set %s=%s" % (path, quote(value)))
    return batch


def uci_value(value):
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        return [uci_scalar(item) for item in value]
    return uci_scalar(value)


def uci_scalar(value):
    if isinstance(value, bool):
        return "1" if value else "0"
    text = str(value)
    if "'" in text or "\n" in text:
        raise AnsibleFilterError("value %r contains a quote or a newline, which uci batch cannot carry, rewrite the value without it" % text)
    return text


def quote(value):
    return "'%s'" % value


def address(package, section):
    if section["name"]:
        return "%s.%s" % (package, section["name"])
    return "%s.@%s[%d]" % (package, section["type"], section["index"])


def require_name(name, kind):
    if not isinstance(name, str) or not NAME.match(name):
        raise AnsibleFilterError("%s name %r is not a valid uci identifier, use letters, digits and underscores only" % (kind, name))


def require_type(section_type):
    if not isinstance(section_type, str) or not TYPE.match(section_type):
        raise AnsibleFilterError("section type %r is not a valid uci type, use letters, digits, underscores and hyphens only" % section_type)


class FilterModule(object):
    def filters(self):
        return {
            "uci_parse_export": uci_parse_export,
            "uci_batch": uci_batch,
            "uci_batch_packages": uci_batch_packages,
            "uci_batch_chunks": uci_batch_chunks,
        }
