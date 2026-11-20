"""Port breakouts and FEC for BISDN Linux switches.

The dictionaries below are the allowed values of bisdn_config_breakouts and
bisdn_config_ports; the role's README documents them and has to change with
them.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

from ansible.errors import AnsibleFilterError

# breakout modes ofdpa-breakout supports: mode -> (lanes, lane speed in G)
BREAKOUT_MODES = {
    "4x10G": (4, 10),
    "4x25G": (4, 25),
}
# SONiC values that leave a port as it is, e.g. 1x100G or 1x100G[40G]
UNCHANGED = re.compile(r"^1x\d+G(\[\d+G(,\d+G)*\])?$")

FEC_MODES = ("none", "rs", "fc")
# FEC mode -> lane speed in G -> clause of "phy control <n> <clause>=true";
# RS-FEC is clause 91 at 100G and clause 108 at 25G, FC-FEC (BASE-R) clause 74
FEC_CLAUSES = {
    "rs": {100: "cl91", 25: "cl108"},
    "fc": {25: "cl74", 10: "cl74"},
}
PORT_KEYS = ("name", "fec")
PORTS_KEYS = ("default_fec", "list")

PORT_NAME = re.compile(r"^port([1-9]\d*)$")
RE_PORTMAP = re.compile(r"^portmap_(\d+)(?:\.0)?=\d+:(\d+)", re.MULTILINE)
RE_DPORT = re.compile(r"^dport_map_port_(\d+)=(\d+)\s*$", re.MULTILINE)


def panel(name):
    """Front panel number of port<N>."""
    m = PORT_NAME.match(str(name))
    if not m:
        raise AnsibleFilterError("%r is not a BISDN front panel port, want port<N>" % (name,))
    return int(m.group(1))


def bisdn_breakouts(breakouts):
    """Validate bisdn_config_breakouts ({port<N>: mode}) and return the breakouts.

    Returns [{"port", "panel", "lanes", "speed"}] sorted by front panel number,
    without the ports that stay as they are.
    """
    if breakouts is None:
        return []
    if not isinstance(breakouts, dict):
        raise AnsibleFilterError("bisdn_config_breakouts must map port<N> to a breakout mode, got %r" % (breakouts,))
    result = []
    for port, mode in breakouts.items():
        n = panel(port)
        if mode in BREAKOUT_MODES:
            lanes, speed = BREAKOUT_MODES[mode]
            result.append(dict(port=port, panel=n, lanes=lanes, speed=speed))
        elif not (isinstance(mode, str) and UNCHANGED.match(mode)):
            raise AnsibleFilterError(
                "%s: breakout %r, want one of %s or 1x<speed>G (unchanged)"
                % (port, mode, ", ".join(sorted(BREAKOUT_MODES)))
            )
    return sorted(result, key=lambda b: b["panel"])


def bisdn_port_map(config_bcm):
    """Map every front panel port of a config.bcm to its logical port and lane speed.

    Returns {"port<N>": {"panel", "logical", "speed"}}; logical ports without a
    dport_map_port entry (internal ports) are left out.
    """
    speeds = {int(logical): int(speed) for logical, speed in RE_PORTMAP.findall(config_bcm or "")}
    ports = {}
    for logical, n in RE_DPORT.findall(config_bcm or ""):
        logical, n = int(logical), int(n)
        if logical not in speeds:
            raise AnsibleFilterError("config.bcm: dport_map_port_%d=%d has no portmap_%d" % (logical, n, logical))
        ports["port%d" % n] = dict(panel=n, logical=logical, speed=speeds[logical])
    if not ports:
        raise AnsibleFilterError("config.bcm has no dport_map_port entries")
    return ports


def fec_mode(value, where):
    if value not in FEC_MODES:
        raise AnsibleFilterError("%s: fec %r, want one of %s" % (where, value, ", ".join(FEC_MODES)))
    return value


def bisdn_fec(ports, port_map):
    """Validate bisdn_config_ports against a port map and return the FEC settings.

    Returns [{"port", "panel", "fec", "speed", "clause"}] sorted by front panel
    number, only for ports with a FEC other than none (BISDN's default).
    default_fec applies to every port whose lane speed supports it; a fec set
    in list must fit the port's speed.
    """
    ports = ports or {}
    if not isinstance(ports, dict):
        raise AnsibleFilterError("bisdn_config_ports must be a dict with default_fec and list, got %r" % (ports,))
    unknown = sorted(set(ports) - set(PORTS_KEYS))
    if unknown:
        raise AnsibleFilterError("bisdn_config_ports: unknown keys %s, want %s" % (", ".join(unknown), ", ".join(PORTS_KEYS)))
    default = fec_mode(ports.get("default_fec", "none"), "bisdn_config_ports.default_fec")

    # the default applies to every port whose speed supports it; a mode set
    # for a port explicitly must fit its speed
    fec = {name: default for name in port_map if port_map[name]["speed"] in FEC_CLAUSES.get(default, {})}
    for i, entry in enumerate(ports.get("list") or []):
        where = "bisdn_config_ports.list[%d]" % i
        if not isinstance(entry, dict) or "name" not in entry:
            raise AnsibleFilterError("%s: want {name: port<N>, fec: ...}, got %r" % (where, entry))
        unknown = sorted(set(entry) - set(PORT_KEYS))
        if unknown:
            raise AnsibleFilterError("%s: unknown keys %s, want %s" % (where, ", ".join(unknown), ", ".join(PORT_KEYS)))
        name = entry["name"]
        if name not in port_map:
            raise AnsibleFilterError(
                "%s: unknown port %r, this switch has %s"
                % (where, name, ", ".join(sorted(port_map, key=lambda p: port_map[p]["panel"])))
            )
        fec[name] = fec_mode(entry.get("fec", default), "%s (%s)" % (where, name))

    result = []
    for name, mode in fec.items():
        if mode == "none":
            continue
        port = port_map[name]
        clause = FEC_CLAUSES[mode].get(port["speed"])
        if clause is None:
            raise AnsibleFilterError(
                "%s: fec %s is not supported at %dG, only at %s"
                % (name, mode, port["speed"], ", ".join("%dG" % s for s in sorted(FEC_CLAUSES[mode])))
            )
        result.append(dict(port=name, panel=port["panel"], fec=mode, speed=port["speed"], clause=clause))
    return sorted(result, key=lambda f: f["panel"])


class FilterModule(object):
    def filters(self):
        return {
            "bisdn_breakouts": bisdn_breakouts,
            "bisdn_port_map": bisdn_port_map,
            "bisdn_fec": bisdn_fec,
        }
