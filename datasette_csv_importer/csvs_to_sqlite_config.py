#!/usr/bin/env python
import re
import json


config_text="""
-s, --separator TEXT         Field separator in input .csv
-q, --quoting INTEGER        Control field quoting behavior per csv.QUOTE_*
                             constants. Use one of QUOTE_MINIMAL (0),
                             QUOTE_ALL (1), QUOTE_NONNUMERIC (2) or
                             QUOTE_NONE (3).
--skip-errors                Skip lines with too many fields instead of
                             stopping the import
--replace-tables             Replace tables if they already exist
-t, --table TEXT             Table to use (instead of using CSV filename)
-c, --extract-column TEXT    One or more columns to 'extract' into a
                             separate lookup table. If you pass a simple
                             column name that column will be replaced with
                             integer foreign key references to a new table
                             of that name. You can customize the name of the
                             table like so:
                                 state:States:state_name
                             This will pull unique values from the 'state'
                             column and use them to populate a new 'States'
                             table, with an id column primary key and a
                             state_name column containing the strings from
                             the original column.
-d, --date TEXT              One or more columns to parse into ISO formatted
                             dates
-dt, --datetime TEXT         One or more columns to parse into ISO formatted
                             datetimes
-df, --datetime-format TEXT  One or more custom date format strings to try
                             when parsing dates/datetimes
-pk, --primary-key TEXT      One or more columns to use as the primary key
-f, --fts TEXT               One or more columns to use to populate a full-
                             text index
-i, --index TEXT             Add index on this column (or a compound index
                             with -i col1,col2)
--shape TEXT                 Custom shape for the DB table - format is
                             csvcol:dbcol(TYPE),...
--filename-column TEXT       Add a column with this name and populate with
                             CSV file name
--no-index-fks               Skip adding index to foreign key columns
                             created using --extract-column (default is to
                             add them)
--no-fulltext-fks            Skip adding full-text index on values extracted
                             using --extract-column (default is to add them)
--just-strings               Import all columns as text strings by default
                             (and, if specified, still obey --shape,
                             --date/datetime, and --datetime-format)
"""


def parse_cli_args():
    args = []
    for line in config_text.split("\n"):
        if not line:
            continue

        if not line.startswith("-"):
            args[-1]["description"] += " "
            args[-1]["description"] += line.strip()
            continue

        # strip out the short command arg version
        if not line.startswith("--"):
            line = line[line.index("--"):]

        # split up the command with (optionsl) argument from description
        cmd_arg, description = re.split(r"\s{2,}", line)

        cmd_arg_parts = re.split(f"\s", cmd_arg)

        n_parts = len(cmd_arg_parts)
        if n_parts == 1:
            args.append({
                "command": cmd_arg_parts[0],
                "args": "",
                "description": description.strip()
            })
        elif n_parts == 2:
            args.append({
                "command": cmd_arg_parts[0],
                "args": cmd_arg_parts[1],
                "description": description.strip()
            })
        else:
            print("Line", line)
            print("cmd_arg", cmd_arg)
            print("description", description)
            print("cmd_arg_parts", cmd_arg_parts)
            raise NotImplementedError(f"Failed parsing line with {n_parts} parts")

    return args


def parsed_to_schema(parsed_args):
    schema = {
        "title": "CSVs-to_SQlite args",
        "description": "CSVs-to-SQlite DB converter arguments",
        "type": "object",
        "properties": {},
    }
    for arg in parsed_args:
        cmd = arg["command"]
        name = re.sub(f"[^a-z\s]+", " ", cmd).strip()
        schema["properties"][cmd] = {
            "type": 'string' if arg["args"] else "boolean",
            "title": name,
            "description": arg["description"],
        }
    return schema


def pprint(*args):
    strs = []
    for arg in args:
        if isinstance(arg, str):
            strs.append(arg)
        else:
            strs.append(json.dumps(arg, indent=2))
    print(" ".join(strs))


if __name__ == "__main__":
    parsed_args = parse_cli_args()
    pprint(parsed_args)
    schema = parsed_to_schema(parsed_args)
    pprint(schema)
