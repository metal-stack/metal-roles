#!/usr/bin/env python3

import argparse
import json
import subprocess


def read_running_config():
    result = subprocess.run(["sonic-cfggen", "-d", "--print-data"],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def merge_fields(running_table, rendered_table):
    merged = {key: dict(fields) for key, fields in running_table.items()}
    for key, fields in rendered_table.items():
        merged.setdefault(key, {}).update(fields)
    return merged


def build_target(running, rendered, merge_tables):
    owned = set(rendered)
    target = {table: content for table, content in running.items() if table not in owned}
    for table, content in rendered.items():
        if table in merge_tables:
            target[table] = merge_fields(running.get(table, {}), content)
        else:
            target[table] = content
    return target


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build a complete config_db target from the running config and a rendered partial config")
    parser.add_argument("--rendered", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--merge-tables", default="DEVICE_METADATA,PORT")
    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.rendered) as handle:
        rendered = json.load(handle)
    merge_tables = {table for table in args.merge_tables.split(",") if table}
    target = build_target(read_running_config(), rendered, merge_tables)
    with open(args.out, "w") as handle:
        json.dump(target, handle, indent=1)


if __name__ == "__main__":
    main()
