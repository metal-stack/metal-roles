#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys


def read_running_config():
    result = subprocess.run(["sonic-cfggen", "-d", "--print-data"],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def find_partial_tables(running, rendered, merge_tables):
    findings = {}
    for table, rendered_content in rendered.items():
        if table in merge_tables:
            continue
        running_content = running.get(table, {})
        if not isinstance(running_content, dict) or not isinstance(rendered_content, dict):
            continue
        for key in sorted(set(running_content) & set(rendered_content)):
            running_key, rendered_key = running_content[key], rendered_content[key]
            if not isinstance(running_key, dict) or not isinstance(rendered_key, dict):
                continue
            missing = tuple(sorted(set(running_key) - set(rendered_key)))
            if missing:
                findings.setdefault(table, {}).setdefault(missing, []).append(key)
    return findings


def report(findings):
    for table, keys_by_fields in sorted(findings.items()):
        for fields, keys in sorted(keys_by_fields.items()):
            sample = ", ".join(keys[:3])
            if len(keys) > 3:
                sample += f" and {len(keys) - 3} more"
            print(f"{table}: {', '.join(fields)} on {sample} exist in the running config "
                  f"but not in the rendered one")
    print("replacing these tables would delete those fields, "
          "add them to sonic_config_merge_tables: " + ", ".join(sorted(findings)))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fail when the rendered config fills a table only in part "
                    "and that table is not listed as one to merge")
    parser.add_argument("--rendered", required=True)
    parser.add_argument("--merge-tables", default="")
    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.rendered) as handle:
        rendered = json.load(handle)
    merge_tables = {table for table in args.merge_tables.split(",") if table}
    findings = find_partial_tables(read_running_config(), rendered, merge_tables)
    if findings:
        report(findings)
        sys.exit(1)


if __name__ == "__main__":
    main()
