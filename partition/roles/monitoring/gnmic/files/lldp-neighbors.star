def apply(*events):
    output = []
    for event in events:
        neighbors = {}
        for path, value in event.values.items():
            segments = path.split("/")
            if len(segments) != 4 or segments[1] != "LLDP_ENTRY_TABLE":
                continue
            _, _, entry_key, field = segments
            if not field.startswith("lldp_rem_"):
                continue
            interface, _, chassis_mac = entry_key.partition(":")
            field = field[len("lldp_rem_"):]
            neighbor = (interface, chassis_mac)
            if neighbor not in neighbors:
                neighbors[neighbor] = {}
            neighbors[neighbor][field] = str(value)

        if len(neighbors) == 0:
            output.append(event)
            continue

        for neighbor, fields in neighbors.items():
            interface, chassis_mac = neighbor
            output.append(Event(
                name = "sonic_lldp_neighbor",
                timestamp = event.timestamp,
                tags = {
                    "source": event.tags.get("source", ""),
                    "interface": interface,
                    "remote_chassis": chassis_mac or fields.get("chassis_id", ""),
                    "remote_system": fields.get("sys_name", ""),
                    "remote_port": fields.get("port_id", ""),
                    "remote_port_desc": fields.get("port_desc", ""),
                },
                values = {"sonic_lldp_neighbor": 1},
            ))
    return output
