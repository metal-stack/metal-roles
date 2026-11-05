#!/usr/bin/env python3
import yaml
import json
import subprocess
import re
import os
from pathlib import Path


def flatten_spec(spec, prefix=""):
    flat = {}
    for var, info in spec.items():
        path = f"{prefix}.{var}" if prefix else var
        desc = info.get('description', '')
        if isinstance(desc, list):
            desc = ' '.join(desc)
        if desc:
            required = info.get('required', False)
            if required:
                desc = "REQUIRED: " + desc
            flat[path] = desc
        if 'options' in info:
            flat.update(flatten_spec(info['options'], path))
    return flat


def add_comments(dumped_yaml, spec):
    flat_spec = flatten_spec(spec)
    lines = dumped_yaml.splitlines()
    result = []

    for line in lines:
        match = re.match(r"^(\s*)([^:\s]+):", line)
        if match:
            indent, key = match.groups()
            description = None
            for path, desc in flat_spec.items():
                if path == key or path.endswith(f".{key}"):
                    description = desc
                    break

            if description:
                result.append(f"{indent}# {description}")

        result.append(line)

    return "\n".join(result)


def update_readme(role_path, yaml_block, dependencies):
    readme_path = role_path / "README.md"

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    var_section_match = re.search(r"(## Variables.*)", content, re.DOTALL)
    if not var_section_match:
        var_section = "## Variables\n\n"
    else:
        var_section = var_section_match.group(1)

    # Remove existing dependency lines to avoid duplication when paths change
    var_section = re.sub(r"^This role depends on default values of.*(?:\n|$)", "", var_section, flags=re.MULTILINE)

    dep_sentences = []
    for dep in dependencies:
        if dep.endswith("roles/defaults"):
            dep_readme = os.path.join(
                dep.removeprefix("metal-roles/"), "README.md")
            relative = os.path.relpath(dep_readme, start=role_path)

            sentence = f"This role depends on default values of [{dep}]({relative})."
            dep_sentences.append(sentence)

    dep_text = "\n\n".join(dep_sentences)

    if "```yaml" in var_section:
        parts = re.split(r"```yaml.*?```", var_section, flags=re.DOTALL)
        prefix = parts[0].rstrip()
        suffix = parts[1].lstrip() if len(parts) > 1 else ""

        if dep_text:
            new_var_section = f"{prefix}\n\n{dep_text}\n\n{yaml_block}\n\n{suffix}".strip(
            )
        else:
            new_var_section = f"{prefix}\n\n{yaml_block}\n\n{suffix}".strip()
    else:
        if dep_text:
            new_var_section = f"{var_section}\n\n{dep_text}\n\n{yaml_block}".strip(
            )
        else:
            new_var_section = f"{var_section}\n\n{yaml_block}".strip()

    new_content = content.replace(var_section, new_var_section)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content + "\n")


def main():
    for specs_file in Path(".").rglob("meta/argument_specs.yaml"):
        role_dir = specs_file.parent.parent
        role_name = role_dir.name

        print(f"Processing role: {role_name} at {role_dir}")

        try:
            result = subprocess.run(
                ["ansible-doc", "-t", "role", "-r",
                    str(role_dir.parent), role_name, "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            role_data = data.get(role_name, {})
            entrypoints = role_data.get("entry_points", {})

            count = 0
            for entrypoint, options in entrypoints.items():
                options = entrypoints.get(entrypoint, {}).get("options", {})
                count += 1

            if count > 1:
                raise Exception("only single entrypoint allowed for now")

        except Exception as e:
            print(
                f"Warning: No argument spec for {role_name} via ansible-doc: {e}")
            continue

        dependencies = []
        for f in Path(role_dir).glob("meta/main.y*ml"):
            with open(f, 'r', encoding='utf-8') as f:
                meta_data = yaml.safe_load(f) or {}
                dependencies = meta_data.get('dependencies', [])
                # handle case where dependencies might be a list of dicts or strings
                if dependencies:
                    dependencies = [d['role'] if isinstance(
                        d, dict) and 'role' in d else d for d in dependencies]
                    break

        defaults = {}
        for f in Path(role_dir / "defaults").rglob("*.y*ml"):
            with open(f, 'r', encoding='utf-8') as f:
                defaults = defaults | yaml.safe_load(f) or {}

        doc_vars = {}
        for key in options:
            doc_vars[key] = None
            if key in defaults:
                doc_vars[key] = defaults[key]

        dumped_yaml = yaml.dump(doc_vars, sort_keys=True,
                                default_flow_style=False, width=1000)

        yaml_content = add_comments(dumped_yaml, options)
        yaml_block = "```yaml\n" + yaml_content + "\n```"

        update_readme(role_dir, yaml_block, dependencies)
        print(f"Updated README.md for {role_name}")


if __name__ == "__main__":
    main()
