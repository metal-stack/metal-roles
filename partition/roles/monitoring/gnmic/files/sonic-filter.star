def apply(*events):
    output = []
    for event in events:
        values = {}
        for name, value in event.values.items():
            if name.startswith("sonic_") or name.startswith("crm_"):
                values[name] = value
        if len(values) == 0:
            continue
        output.append(Event(
            name = event.name,
            timestamp = event.timestamp,
            tags = event.tags,
            values = values,
        ))
    return output
