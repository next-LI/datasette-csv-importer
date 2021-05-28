# datasette-csv-importer

A Datasette plugin for live-uploading CSV files with a user-friendly configuration UI that doesn't require the application to be restarted to work.

This plugin was inspired by the [datasette-upload-csvs](https://github.com/simonw/datasette-upload-csvs) plugin and uses [CSVs-to-SQlite](https://github.com/simonw/csvs-to-sqlite) to actually perform the import. Configuration comes from a parsed version of the CLI tool's `--help` output.

## Installation

This repository uses submodules:

    git clone --recursive https://github.com/next-LI/datasette-csv-importer

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
- `csvs_path` - path to the directory where raw uploaded CSVs will be saved, along with their `csvs-to-sqlite` import settings. If this isn't set, then this plugin won't do CSV/config saving.
- `use_db_metadata` - (boolean)  Whether or not to build the `__metadata` table as supported by the [next-LI/datasette_live_config](https://github.com/next-LI/datasette_live_config) plugin, giving default access to the current user.
- `use_live_permissions` - (boolean) Whether or not to integrate with the [next-LI/datasette-live-permissions](https://github/com/next-LI/datasette-live-permissions) and grant the uploading user access upon upload.


## Usage

**tl;dr**: Go to `/-/csv-importer`, select a CSV, choose import options, click submit 💥 and your data is live on the dashboard!

The plugin adds an interface at `/-/csv-importer` for importing a CSV file. Once you drag and drop a CSV file, you'll be shown a set of options for importing your data into Datasette using the [CSVs-to-SQlite](https://github.com/simonw/csvs-to-sqlite) tool. Clicking "Submit" below will start the import process and you'll be given information about success or failure.

## Development

There's two parts to this plugin: converting the CSV importer CLI tool's arguments list to a JSON schema which renders a form (this is mostly done by hand and ends up in `templates/schema.json` and the webapp that does the actual import.

### KNOWN ISSUES

There's an async race condition that can sometimes be triggered when uploading and inserting a new database. You'll get a 500 error and a console traceback like the following:

```
INFO:     127.0.0.1:52790 - "POST /-/csv-importer HTTP/1.1" 200 OK
/Users/brandon/.pyenv/versions/nextli/lib/python3.8/site-packages/pandas/core/generic.py:2779: UserWarning: The spaces in these column names will not be changed. In pandas versions < 0.14, spaces were converted to underscores.
  sql.to_sql(
There is no current event loop in thread 'Thread-2'.
Traceback (most recent call last):
  File "/Users/brandon/.pyenv/versions/nextli/lib/python3.8/site-packages/datasette-0.56-py3.8.egg/datasette/app.py", line 1144, in route_path
    response = await view(request, send)
  File "/Users/brandon/.pyenv/versions/nextli/lib/python3.8/site-packages/datasette-0.56-py3.8.egg/datasette/views/base.py", line 146, in view
    return await self.dispatch_request(
  File "/Users/brandon/.pyenv/versions/nextli/lib/python3.8/site-packages/datasette-0.56-py3.8.egg/datasette/views/base.py", line 119, in dispatch_request
    await self.ds.refresh_schemas()
  File "/Users/brandon/.pyenv/versions/nextli/lib/python3.8/site-packages/datasette-0.56-py3.8.egg/datasette/app.py", line 343, in refresh_schemas
    for database_name, db in self.databases.items():
RuntimeError: OrderedDict mutated during iteration
```

As far as I can tell, you can ignore this error. If your import got to the point where this bug can be triggered, your data was successfully imported.
