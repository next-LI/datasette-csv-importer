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

{
    "type": "object",
    "patternProperties": {
        r"^[A-Za-z0-9_\-]+$": {
            "type": "object",
            "title": "Database name",
            "description": "Database to configure",
            "properties": {
                "source": {
                    "type": "string",
                    "title": "Source",
                    "description": "Where this data came from?"
                },
                "source_url": {
                    "type": "string",
                    "title": "Source URL",
                    "description": "URL to info about source",
                    "examples": ["https://example.tld"],
                },
                "tables": {
                    "type": "object",
                    "patternProperties": {
                        r"^[A-Za-z0-9_\-]+$": {
                            "type": "object",
                            "title": "Table name",
                            "descriptions": "Table within this database to configure",
                            "properties": {
                                "description_html": {
                                    "type": "string",
                                },
                                "license": {
                                    "type": "string",
                                    "example": "CC BY 3.0 US",
                                },
                                "license_url": {
                                    "type": "string",
                                    "example": "https://creativecommons.org/licenses/by/3.0/us/",
                                },

                                "hidden": {
                                    "type": "boolean",
                                    "default": False,
                                    "description": "tables can be hidden using this",
                                },

                                "label_column": {
                                    "type": "object",
                                    "title": "column name",
                                    "description": "this controls which column is used as the link to the detail view",
                                },

                                "size": {
                                    "type": "number",
                                    "title": "Page size",
                                    "description": "How many table records to display per page",
                                    "default": 10,
                                },

                                "sort": {
                                    "type": "string",
                                    "title": "Default sort column",
                                },
                                "sort_desc": {
                                    "type": "string",
                                    "title": "Default descending sort column",
                                    "description": "Can't use with sort",
                                },
                                "sortable_columns": {
                                    "type": "array",
                                    "title": "Sortable columns",
                                    "description": "If used, any columns not in this list will not be sortable",
                                    "items": {
                                        "type": "string"
                                    },
                                    "default": [],
                                },

                                "facets": {
                                    "type": "array",
                                    "title": "Fascet columns",
                                    "description": "List of columns to enable faceting on",
                                    "items": {
                                        "type": "string",
                                    }
                                },

                                "units": {
                                    "type": "object",
                                    "title": "Column units",
                                    "description": "A full list of units is available in metadata-units-list.txt",
                                    "patternProperties": {
                                        r"^[A-Za-z0-9_\-]+$": {
                                            "type": "string",
                                            "title": "Unit",
                                        },
                                    },
                                    "additionalProperties": False,
                                },

                                "queries": {
                                    "type": "object",
                                    "patternProperties": {
                                        r"^[A-Za-z0-9_\-]+$": {
                                            "type": "object",
                                            "properties": {
                                                "sql": {
                                                    "type": "string",
                                                    "title": "Canned query SQL",
                                                    "examples": [
                                                        "select neighborhood, facet_cities.name, state\nfrom facetable\n  join facet_cities on facetable.city_id = facet_cities.id\nwhere neighborhood like '%' || :text || '%'\norder by neighborhood",
                                                        "select  'fixtures' as database, * from  [fixtures].sqlite_master union select  'extra_database' as database, * from  [extra_database].sqlite_master",
                                                    ]
                                                },
                                                "fragment": {
                                                    "type": "string",
                                                    "title": "Fragment string",
                                                    "description": "Some plugins accept additional config via the URL hash, this sets the default hash 'fragment' to use",
                                                },
                                                "title": {
                                                    "type": "string",
                                                    "description": "Optional display name of canned query",
                                                },
                                                "description": {
                                                    "type": "string",
                                                    "description": "Optional description of canned query",
                                                }
                                            }
                                        }
                                    },
                                    "additionalProperties": False,
                                }
                            }
                        }
                    },
                    "additionalProperties": False,
                }
            }
        }
    },
    "additionalProperties": False,
    "title": "Databases",
}


metadata_config_example = {
  "databases": {
    "database name": {
      # optional, where this data came from
      "source": "Alternative source",
      # optional, URL to info about source
      "source_url": "http://example.com/",
      # table-speicific config
      "tables": {
        "table name": {
          # tables can be hidden using this
          "hidden": False,
          # you can also nest down a layer for views
          "name of view": {},
          # this controls which column is used as the link to the detail view
          "label_column": "column name",
          # page size
          "size": 10,
          # you can only use one of the two
          "sort": "Column name",
          "sort_desc": "Column Name",
          # columns available for sorting, this is restrictive and
          # leaving this option out allows all columns to be sorted
          "sortable_columns": [
              "height",
              "weight"
          ],
          # facets can be turned on by default here (they can always be
          # enabled via URL query param, unless disabled)
          "facets": ["column name"],
          # a full list of units is available in metadata-units-list.txt
          "units": {
            "column name": "metres",
            "column name 2": "Hz"
          },
          "description_html": "Custom <em>table</em> description",
          "license": "CC BY 3.0 US",
          "license_url": "https://creativecommons.org/licenses/by/3.0/us/",
          # canned queries
          "queries": {
            "canned query name": {
              # simple static SQL example
              "sql": "select column_name from table_name",
              # example with params (text is the param here)
              "sql": "select neighborhood, facet_cities.name, state\nfrom facetable\n  join facet_cities on facetable.city_id = facet_cities.id\nwhere neighborhood like '%' || :text || '%'\norder by neighborhood",
              # cross-DB canned query example
              "sql": "select  'fixtures' as database, * from  [fixtures].sqlite_master union select  'extra_database' as database, * from  [extra_database].sqlite_master",
              # some plugins accept additional config via the URL hash, this sets the
              # default hash "fragment" to use
              "fragment": "fragment-goes-here",
              "title": "Optional display name of canned query",
              "description": "Optional description of canned query"
            }
          }
        }
      }
    }
  }
}


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
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/product.schema.json",
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

    example_to_schema
