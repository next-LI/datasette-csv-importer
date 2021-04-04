import { h, Component } from "preact";
import Form from "react-jsonschema-form";
//import "./style.scss";

const schema = {
  "title": "CSVs-to_SQlite args",
  "description": "CSVs-to-SQlite DB converter arguments",
  "type": "object",
  "properties": {
    "--separator": {
      "type": "string",
      "title": "separator",
      "description": "Field separator in input .csv"
    },
    "--quoting": {
      "type": "string",
      "title": "quoting",
      "description": "Control field quoting behavior per csv.QUOTE_* constants. Use one of QUOTE_MINIMAL (0), QUOTE_ALL (1), QUOTE_NONNUMERIC (2) or QUOTE_NONE (3)."
    },
    "--skip-errors": {
      "type": "boolean",
      "title": "skip errors",
      "description": "Skip lines with too many fields instead of stopping the import"
    },
    "--replace-tables": {
      "type": "boolean",
      "title": "replace tables",
      "description": "Replace tables if they already exist"
    },
    "--table": {
      "type": "string",
      "title": "table",
      "description": "Table to use (instead of using CSV filename)"
    },
    "--extract-column": {
      "type": "string",
      "title": "extract column",
      "description": "One or more columns to 'extract' into a separate lookup table. If you pass a simple column name that column will be replaced with integer foreign key references to a new table of that name. You can customize the name of the table like so: state:States:state_name This will pull unique values from the 'state' column and use them to populate a new 'States' table, with an id column primary key and a state_name column containing the strings from the original column."
    },
    "--date": {
      "type": "string",
      "title": "date",
      "description": "One or more columns to parse into ISO formatted dates"
    },
    "--datetime": {
      "type": "string",
      "title": "datetime",
      "description": "One or more columns to parse into ISO formatted datetimes"
    },
    "--datetime-format": {
      "type": "string",
      "title": "datetime format",
      "description": "One or more custom date format strings to try when parsing dates/datetimes"
    },
    "--primary-key": {
      "type": "string",
      "title": "primary key",
      "description": "One or more columns to use as the primary key"
    },
    "--fts": {
      "type": "string",
      "title": "fts",
      "description": "One or more columns to use to populate a full- text index"
    },
    "--index": {
      "type": "string",
      "title": "index",
      "description": "Add index on this column (or a compound index with -i col1,col2)"
    },
    "--shape": {
      "type": "string",
      "title": "shape",
      "description": "Custom shape for the DB table - format is csvcol:dbcol(TYPE),..."
    },
    "--filename-column": {
      "type": "string",
      "title": "filename column",
      "description": "Add a column with this name and populate with CSV file name"
    },
    "--no-index-fks": {
      "type": "boolean",
      "title": "no index fks",
      "description": "Skip adding index to foreign key columns created using --extract-column (default is to add them)"
    },
    "--no-fulltext-fks": {
      "type": "boolean",
      "title": "no fulltext fks",
      "description": "Skip adding full-text index on values extracted using --extract-column (default is to add them)"
    },
    "--just-strings": {
      "type": "boolean",
      "title": "just strings",
      "description": "Import all columns as text strings by default (and, if specified, still obey --shape, --date/datetime, and --datetime-format)"
    }
  }
};

const unitSchema = {
  "type": "object",
  "properties": {
    /* We're gonna convert this one to a simple object key (string) => value (string) format */
    "_name": {
      "title": "Column name",
      "description": "Enter the column name to set unit for.",
      "type": "string",
    },
    "_value": {
      "title": "Unit",
      "description": "Enter a unit the values in the column should be displayed as. A full list of values can be foud here: https://github.com/hgrecco/pint/blob/master/pint/default_en.txt",
      "type": "string",
    }
  }
};

const querySchema = {
  "type": "object",
  "properties": {
    /* Any object with a _name and no _value key, gets turned into an object
     * where the _name is the parent key containing the object otherwise described
     * below. This is true for all the schema with the exception of unitSchema.
     **/
    "_name": {
      "title": "Query name",
      "description": "Enter a descriptive name for this canned query.",
      "type": "string",
    },
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
      "title": "Friendly name",
      "description": "Optional display name of canned query. This can be 'friendlier' than the query name above and can include quotes, spaces, etc.",
      "type": "string",
    },
    "description": {
      "title": "Description",
      "description": "Optional description of canned query",
      "type": "string",
    }
  }
};

const tableSchema = {
  "type": "object",
  "title": "Table name",
  "descriptions": "Table within this database to configure",
  "properties": {
    "_name": {
      "title": "Table name",
      "description": "Enter the name of the table to configure",
      "type": "string",
    },
    "description_html": {
      "title": "Table description",
      "description": "Enter a description of the table to show users. This may contain HTML.",
      "type": "string",
    },
    "license": {
      "title": "license",
      "type": "string",
      "examples": [
        "CC BY 3.0 US", "Copyright Company Name. All rights reserved."
      ],
    },
    "license_url": {
      "title": "License URL",
      "description": "A URL to the full license terms, if applicable.",
      "type": "string",
      "examples": [
        "https://creativecommons.org/licenses/by/3.0/us/",
      ]
    },

    "hidden": {
      "title": "Hidden?",
      "description": "tables can be hidden using this option.",
      "type": "boolean",
      "default": false,
    },

    "label_column": {
      "title": "Label column",
      "description": "Enter the name of the column to use as the link to the individual record page. By default the first column, which is the CSV row number, will be used. Set this to override this default.",
      "type": "string",
    },

    "size": {
      "title": "Page size",
      "description": "How many table records to display per page.",
      "type": "number",
      "default": 10,
    },

    "sort": {
      "title": "Default sort column (ascending)",
      "type": "string",
    },
    "sort_desc": {
      "title": "Default sort column (descending)",
      "description": "Can't use with default ascending sort",
      "type": "string",
    },

    "sortable_columns": {
      "title": "Sortable columns",
      "description": "If used, any columns not in this list will not be sortable",
      "type": "array",
      "items": {
        "type": "string",
        "title": "Column name",
      },
      "default": [],
    },

    "facets": {
      "title": "Fascet columns",
      "description": "List of columns to enable faceting on",
      "type": "array",
      "items": {
        "type": "string",
        "title": "Column name",
      }
    },

    "units": {
      "type": "array",
      "title": "Column units",
      "items": unitSchema
    },

    "queries": {
      "type": "array",
      "title": "Canned queries",
      "items": querySchema,
    }
  }
};

const metaSchema = {
  "title": "Databases",
  "description": "This lets you control database settings for tables, queries, units, and various display and analysis related options. If you don't see any databases below, it's because no databases are currently configured. You add a database configuration by clicking the plus button.",
  "type": "array",
  "items": {
    "title": "Database",
    "description": "Database to configure",
    "type": "object",
    "properties": {
      "_name": {
        "title": "Database name",
        "description": "Enter the name of a database to configure.",
        "type": "string",
      },
      "source": {
        "title": "Source",
        "description": "Where this data came from?",
        "type": "string",
      },
      "source_url": {
        "title": "Source URL",
        "description": "URL to info about source",
        "type": "string",
        "examples": ["https://example.tld"],
      },
      "description": {
        "title": "Database description",
        "description": "Enter a description of the database to show users. This may contain HTML.",
        "type": "string",
      },
      "tables": {
        "title": "Database Table",
        "description": "Add or select a database table to configure",
        "type": "array",
        "items": tableSchema
      }
    }
  },
};

export default class App extends Component {
  render(props) {
    return (
      <div class="editor-widget">
        <h1 style={{ color: props.color }}>Configuration Options</h1>
        <Form schema={schema}
              onChange={(data, e) => {
                console.log("CSV Config Changed", data, e);
              }}
              onSubmit={(data, e) => {
                console.log("CSV Config Submitted", data, e);
              }}
              onError={(data, e) => {
                console.log("CSV Config Error", data, e);
              }} />
        <Form schema={metaSchema}
              onChange={(data, e) => {
                console.log("Datasette Config Changed", data, e);
              }}
              onSubmit={(data, e) => {
                console.log("Datasette Config Submitted", data, e);
              }}
              onError={(data, e) => {
                console.log("Datasette Config Error", data, e);
              }} />
      </div>
    );
  }
}
