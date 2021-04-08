# datasette-csv-importer

Datasette plugin for live-uploading CSV files with a user-friendly configuration UI that doesn't require the application to be restarted to work.

This plugin was inspired by the [datasette-upload-csvs](https://github.com/simonw/datasette-upload-csvs)
plugin and uses [CSVs-to-SQlite](https://github.com/simonw/csvs-to-sqlite) to actually perform the import.
Configuration comes from a parsed version of the CLI tool's `--help` output.

## Installation

This repository uses submodules:

    git clone --recursive https://github.com/brandonrobertz/datasette-csv-importer

If you've already cloned non-recursively you can run this to get the submodules:

    git submodule update --init

Then just install like any normal Datasette plugin:

    python setup.py install

It accepts the following configuration in your `metadata.json` file:

    {
      ... metadata.json ...
      "plugins": {
        "datasette-csv-importer": {
          "status_table": "_csv_importer_progress_",
          "status_database": "_internal",
          "database_path": "/data"
        },
        ... the rest of your plugins configuration ...
      }
    }

Details on the configuration:

- `status_database` - name of the database that we're going to use to store import status. It defaults to the internal DB, `_internal`.
- `status_table` - name of the table that we'll write import status rows to.
- `database_path` - path to the directory that we'll use to write SQlite databases to. By default, the plugin will use the current working directory of the process running it.



## Usage

The plugin adds an interface at `/-/csv-importer` for uploading a CSV file
and modifying import configuration options like column types, full text
fields, primary and foreign keys. A full list of configuration options
comes from the [CSVs-to-SQlite](https://github.com/simonw/csvs-to-sqlite)
tool used by this plugin.


## Development

There's two parts to this plugin: converting the CSV importer CLI tool's arguments
list to a JSON schema which renders a form (this is mostly done by hand and ends up
in `templates/schema.json` and the webapp that does the actual import.
