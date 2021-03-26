# datasette-git-importer

Datasette plugin for uploading CSV files, editing configuration and creating commits representing the changes.

This plugin is based on the [datasette-upload-csvs](https://github.com/simonw/datasette-upload-csvs) plugin.

## Installation

    python setup.py install

## Usage

The plugin adds an interface at `/-/git-importer` for uploading a CSV file, setting meta configuration and pushing a commit to a specified repo.
