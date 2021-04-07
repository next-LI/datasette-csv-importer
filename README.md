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
