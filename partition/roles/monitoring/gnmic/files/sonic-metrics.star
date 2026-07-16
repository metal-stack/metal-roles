BYTE_AND_CRC_COUNTERS = {
    "IF_IN_OCTETS": "sonic_interface_received_bytes_total",
    "IF_OUT_OCTETS": "sonic_interface_transmitted_bytes_total",
    "ETHER_STATS_CRC_ALIGN_ERRORS": "sonic_interface_receive_error_crc_total",
}

RECEIVE_ERROR_TYPES = {
    "IF_IN_ERRORS": "error",
    "IF_IN_DISCARDS": "discard",
    "IN_DROPPED_PKTS": "drop",
    "PAUSE_RX_PKTS": "pause",
}

TRANSMIT_ERROR_TYPES = {
    "IF_OUT_ERRORS": "error",
    "IF_OUT_DISCARDS": "discard",
    "PAUSE_TX_PKTS": "pause",
}

PACKET_METHODS = ["UCAST", "BROADCAST", "MULTICAST"]

PSU_MEASUREMENTS = {
    "input_voltage": "sonic_hw_psu_input_voltage_volts",
    "input_current": "sonic_hw_psu_input_current_amperes",
    "output_voltage": "sonic_hw_psu_output_voltage_volts",
    "output_current": "sonic_hw_psu_output_current_amperes",
    "temp": "sonic_device_psu_celsius",
}

SENSOR_THRESHOLDS = {
    "high_threshold": "high",
    "low_threshold": "low",
    "high_critical_threshold": "high_critical",
    "low_critical_threshold": "low_critical",
}

ROUTE_FIELDS = [
    "ifname", "nexthop", "protocol", "weight", "distance", "metric",
    "blackhole", "vni_label", "router_mac", "segment", "seg6local_action", "nexthop_group",
]

DEVICE_INFO_FIELDS = ["hwsku", "platform", "mac", "type", "hostname"]
PORT_INFO_FIELDS = ["alias", "index", "speed", "mtu"]
PSU_INFO_FIELDS = ["serial", "model", "name"]
TRANSCEIVER_INFO_FIELDS = ["vendor", "manufacturer", "serial", "model"]


def to_number(value):
    if type(value) == "int" or type(value) == "float":
        return value
    text = str(value)
    digits = text[1:] if text.startswith("-") else text
    parts = digits.split(".")
    if len(parts) > 2 or len(digits) == 0:
        return None
    for part in parts:
        if not part.isdigit():
            return None
    return int(text) if len(parts) == 1 else float(text)


def first_digits(text):
    digits = ""
    for i in range(len(text)):
        if text[i].isdigit():
            digits += text[i]
        elif len(digits) > 0:
            break
    return digits if len(digits) > 0 else text


def is_ethernet_port(name):
    return name.startswith("Ethernet") and name[len("Ethernet"):].isdigit()


def table_entries(event, table):
    entries = []
    for path, value in event.values.items():
        segments = path.split("/")
        if len(segments) == 4 and segments[1] == table:
            entries.append((segments[2], segments[3], value))
    return entries


def grouped_fields(event, table):
    groups = {}
    for key, field, value in table_entries(event, table):
        groups.setdefault(key, {})[field] = str(value)
    return groups


def emit(output, event, extra_tags, metric, value):
    tags = dict(event.tags)
    tags.update(extra_tags)
    output.append(Event(name=event.name, timestamp=event.timestamp, tags=tags, values={metric: value}))


def ether_frame_size(stat, prefix):
    if not stat.startswith(prefix) or not stat.endswith("_OCTETS"):
        return None
    if not stat[len(prefix)].isdigit():
        return None
    size = stat[:-len("_OCTETS")].split("_")[-1]
    return size if size.isdigit() else None


def port_counter_metric(stat):
    if stat in BYTE_AND_CRC_COUNTERS:
        return (BYTE_AND_CRC_COUNTERS[stat], {})
    if stat in RECEIVE_ERROR_TYPES:
        return ("sonic_interface_receive_error_input_packets_total", {"type": RECEIVE_ERROR_TYPES[stat]})
    if stat in TRANSMIT_ERROR_TYPES:
        return ("sonic_interface_transmit_error_output_packets_total", {"type": TRANSMIT_ERROR_TYPES[stat]})
    for method in PACKET_METHODS:
        if stat == "IF_IN_" + method + "_PKTS":
            return ("sonic_interface_received_packets_total", {"method": method.lower()})
        if stat == "IF_OUT_" + method + "_PKTS":
            return ("sonic_interface_transmitted_packets_total", {"method": method.lower()})
    size = ether_frame_size(stat, "ETHER_IN_PKTS_")
    if size != None:
        return ("sonic_interface_received_ethernet_packets_total", {"size": size})
    size = ether_frame_size(stat, "ETHER_OUT_PKTS_")
    if size != None:
        return ("sonic_interface_transmitted_ethernet_packets_total", {"size": size})
    return None


def handle_port_counters(event, output):
    for interface, field, value in table_entries(event, "COUNTERS"):
        if not is_ethernet_port(interface) or not field.startswith("SAI_PORT_STAT_"):
            continue
        number = to_number(value)
        if number == None:
            continue
        metric_and_tags = port_counter_metric(field[len("SAI_PORT_STAT_"):])
        if metric_and_tags == None:
            continue
        metric, tags = metric_and_tags
        tags["interface"] = interface
        emit(output, event, tags, metric, number)


def handle_queue_counters(event, output):
    for path, value in event.values.items():
        segments = path.split("/")
        if len(segments) != 6 or segments[1] != "COUNTERS" or segments[3] != "Queues":
            continue
        interface = segments[2]
        queue = segments[4].partition(":")[2]
        if not is_ethernet_port(interface) or not queue.isdigit():
            continue
        if segments[5] == "SAI_QUEUE_STAT_PACKETS":
            metric = "sonic_interface_queue_processed_packets_total"
        elif segments[5] == "SAI_QUEUE_STAT_BYTES":
            metric = "sonic_interface_queue_processed_bytes_total"
        else:
            continue
        number = to_number(value)
        if number != None:
            emit(output, event, {"interface": interface, "queue": queue}, metric, number)


def handle_crm(event, output):
    if "/CRM/STATS/crm_stats_ipv4_route_used" not in event.values:
        return
    total = 0
    for family in ["crm_stats_ipv4_route_used", "crm_stats_ipv6_route_used"]:
        for path, value in event.values.items():
            if path.endswith(family):
                number = to_number(value)
                total += number if number != None else 0
                break
    emit(output, event, {}, "sonic_routes_fib", total)


def emit_used_with_available(output, event, fields, metric_prefix):
    for field, value in fields.items():
        if not field.endswith("_used"):
            continue
        used = to_number(value)
        if used == None:
            continue
        tags = {}
        available = fields.get(field[:-len("_used")] + "_available")
        if available != None:
            tags["available"] = str(available)
        emit(output, event, tags, metric_prefix + field, used)


def handle_crm_stats(event, output):
    for key, fields in grouped_fields(event, "CRM").items():
        if key == "STATS":
            emit_used_with_available(output, event, fields, "")


def handle_crm_acl(event, output):
    groups = {}
    for path, value in event.values.items():
        segments = path.split("/")
        if len(segments) == 5 and segments[1] == "CRM" and segments[2] == "ACL_STATS":
            groups.setdefault(segments[3], {})[segments[4]] = str(value)
        elif len(segments) == 6 and segments[1] == "CRM" and segments[2] == "ACL_STATS":
            groups.setdefault(segments[3] + ":" + segments[4], {})[segments[5]] = str(value)
    for table, fields in groups.items():
        prefix = "crm_acl_stats_" + table.replace(":", "_").lower() + "_"
        emit_used_with_available(output, event, fields, prefix)


def handle_port_status(event, output):
    for interface, field, value in table_entries(event, "PORT_TABLE"):
        up = 1 if str(value) == "up" else 0
        if field == "admin_status":
            emit(output, event, {"interface": interface}, "sonic_interface_admin_status", up)
        elif field == "oper_status":
            emit(output, event, {"interface": interface}, "sonic_interface_operational_status", up)


def handle_routes(event, output):
    routes = {}
    for path in event.values.keys():
        if not path.startswith("/ROUTE_TABLE/"):
            continue
        route = path
        for field in ROUTE_FIELDS:
            if path.endswith("/" + field):
                route = path[:-(len(field) + 1)]
                break
        routes[route] = True
    if len(routes) > 0:
        emit(output, event, {}, "sonic_routes_rib", len(routes))


def handle_port_config(event, output):
    for interface, field, value in table_entries(event, "PORT"):
        number = to_number(value)
        if number == None:
            continue
        if field == "mtu":
            emit(output, event, {"interface": interface}, "sonic_interface_mtu_bytes", number)
        elif field == "speed":
            emit(output, event, {"interface": interface}, "sonic_interface_speed_bytes", number * 125000)
    for interface, fields in grouped_fields(event, "PORT").items():
        tags = {"interface": interface}
        for field in PORT_INFO_FIELDS:
            if field in fields:
                tags[field] = fields[field]
        emit(output, event, tags, "sonic_interface_info", 1)


def handle_device_info(event, output):
    prefix = "/DEVICE_METADATA/localhost/"
    if not has_key_starting(event, prefix):
        return
    tags = {}
    for field in DEVICE_INFO_FIELDS:
        if prefix + field in event.values:
            tags[field] = str(event.values[prefix + field])
    emit(output, event, tags, "sonic_device_info", 1)


def handle_ntp(event, output):
    prefix = "/NTP/global/"
    tags = {}
    for path, value in event.values.items():
        if path.startswith(prefix):
            tags[path.split("/")[-1]] = str(value)
    if len(tags) > 0:
        emit(output, event, tags, "sonic_ntp_global", 1)


def has_key_starting(event, prefix):
    for path in event.values.keys():
        if path.startswith(prefix):
            return True
    return False


def has_key_containing(event, needle):
    for path in event.values.keys():
        if needle in path:
            return True
    return False


def find_number_by_suffix(event, suffix):
    for path, value in event.values.items():
        if path.endswith(suffix):
            return to_number(value)
    return None


def handle_memory(event, output):
    if not has_key_containing(event, "meminfo"):
        return
    total = find_number_by_suffix(event, "mem_total")
    available = find_number_by_suffix(event, "mem_available")
    if total != None and available != None and total > 0:
        emit(output, event, {}, "sonic_device_memory_ratio", (total - available) / total)


def handle_cpu(event, output):
    number = find_number_by_suffix(event, "cpu_all/5min")
    if number != None:
        emit(output, event, {}, "sonic_device_cpu_ratio", number / 100)


def handle_system_status(event, output):
    for path, value in event.values.items():
        if path == "/SYSTEM_READY/SYSTEM_STATE/Status":
            emit(output, event, {}, "sonic_system_status", 1 if str(value).lower() == "up" else 0)


def handle_chassis(event, output):
    tags = {}
    for chassis, field, value in table_entries(event, "CHASSIS_INFO"):
        tags[field] = str(value)
    if len(tags) > 0:
        emit(output, event, tags, "sonic_hw_chassis_info", 1)


def handle_psu(event, output):
    for psu, field, value in table_entries(event, "PSU_INFO"):
        slot = {"slot": first_digits(psu)}
        if field == "status":
            emit(output, event, slot, "sonic_device_psu_operational_status", 1 if str(value).lower() in ["true", "ok"] else 0)
        elif field == "presence":
            emit(output, event, slot, "sonic_device_psu_available_status", 1 if str(value).lower() == "true" else 0)
        elif field in PSU_MEASUREMENTS:
            number = to_number(value)
            if number != None:
                emit(output, event, slot, PSU_MEASUREMENTS[field], number)
    for psu, fields in grouped_fields(event, "PSU_INFO").items():
        tags = {"slot": first_digits(psu)}
        for field in PSU_INFO_FIELDS:
            if field in fields:
                tags[field] = fields[field]
        emit(output, event, tags, "sonic_device_psu_info", 1)


def handle_fans(event, output):
    for fan, field, value in table_entries(event, "FAN_INFO"):
        name = {"name": fan}
        if field == "status":
            emit(output, event, name, "sonic_device_fan_operational_status", 1 if str(value).lower() in ["true", "ok"] else 0)
        elif field == "presence":
            emit(output, event, name, "sonic_device_fan_available_status", 1 if str(value).lower() == "true" else 0)
        elif field == "speed":
            number = to_number(value)
            if number != None:
                emit(output, event, name, "sonic_device_fan_rpm", number)


def handle_temperatures(event, output):
    for sensor, field, value in table_entries(event, "TEMPERATURE_INFO"):
        number = to_number(value)
        if number == None:
            continue
        if field == "temperature":
            emit(output, event, {"name": sensor}, "sonic_device_sensor_celsius", number)
        elif field in SENSOR_THRESHOLDS:
            emit(output, event, {"name": sensor, "threshold": SENSOR_THRESHOLDS[field]}, "sonic_device_sensor_threshold_celsius", number)


def handle_vxlan(event, output):
    if has_key_starting(event, "/VXLAN_TUNNEL_TABLE/"):
        vteps = {}
        for path in event.values.keys():
            if path.startswith("/VXLAN_TUNNEL_TABLE/EVPN_"):
                vteps[path[len("/VXLAN_TUNNEL_TABLE/"):].split("/")[0]] = True
        emit(output, event, {}, "sonic_evpn_remote_vteps", len(vteps))
    for vtep, field, value in table_entries(event, "VXLAN_TUNNEL_TABLE"):
        if field != "operstatus":
            continue
        up = 1 if str(value) == "oper_up" else 0
        is_evpn = vtep.startswith("EVPN_")
        plain = vtep[len("EVPN_"):] if is_evpn else vtep
        emit(output, event, {"vtep": plain}, "sonic_vxlan_operational_status", up)
        if is_evpn:
            emit(output, event, {"vtep": plain}, "sonic_evpn_status", up)


def handle_transceiver_sensors(event, output):
    for interface, field, value in table_entries(event, "TRANSCEIVER_DOM_SENSOR"):
        number = to_number(value)
        if number == None:
            continue
        if field == "temperature":
            emit(output, event, {"interface": interface}, "sonic_interface_transceiver_temperature_celsius", number)
        elif field == "voltage":
            emit(output, event, {"interface": interface}, "sonic_interface_transceiver_voltage", number)
        elif len(field) == 8 and field[:2] in ["rx", "tx"] and field[2].isdigit() and field.endswith("power"):
            direction = "receive" if field[:2] == "rx" else "transmit"
            emit(output, event, {"interface": interface, "lane": field[2]}, "sonic_interface_optic_" + direction + "_power_dbm", number)


def handle_transceiver_info(event, output):
    for interface, fields in grouped_fields(event, "TRANSCEIVER_INFO").items():
        length = to_number(fields.get("cable_length", ""))
        if length != None:
            tags = {
                "interface": interface,
                "cable_type": fields.get("connector", "").lower(),
                "connector_type": fields.get("connector_type", "").lower(),
            }
            emit(output, event, tags, "sonic_interface_cable_length_meters", length)
        tags = {"interface": interface}
        for field in TRANSCEIVER_INFO_FIELDS:
            if field in fields:
                tags[field] = fields[field]
        emit(output, event, tags, "sonic_interface_transceiver_info", 1)


def handle_transceiver_thresholds(event, output):
    for interface, fields in grouped_fields(event, "TRANSCEIVER_DOM_THRESHOLD").items():
        tags = {"interface": interface}
        tags.update(fields)
        emit(output, event, tags, "sonic_transceiver_threshold_info", 1)


HANDLERS = {
    "counters-ports": [handle_port_counters],
    "counters-queues": [handle_queue_counters],
    "counters-crm": [handle_crm, handle_crm_stats],
    "counters-crm-acl": [handle_crm_acl],
    "appl": [handle_port_status, handle_routes],
    "cfg-core": [handle_port_config, handle_device_info, handle_ntp],
    "state-system": [handle_system_status, handle_chassis],
    "state-temperature": [handle_temperatures],
    "state-psu": [handle_psu],
    "state-fan": [handle_fans],
    "state-transceivers": [handle_transceiver_sensors, handle_transceiver_info, handle_transceiver_thresholds],
    "state-vxlan": [handle_vxlan],
    "others": [handle_memory, handle_cpu],
}


def apply(*events):
    output = list(events)
    for event in events:
        for handler in HANDLERS.get(event.name, []):
            handler(event, output)
    return output
