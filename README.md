# datasette-git-importer

Datasette plugin for uploading CSV files, editing configuration and creating commits representing the changes.

This plugin is based on the [datasette-upload-csvs](https://github.com/simonw/datasette-upload-csvs) plugin.

## Installation

    python setup.py install

## Configuration

Plugin secrets used:

    github_user - github user associated with token w/ access to repo
    github_token - github token, gives access to below repo
    repo_owner - owner of repository in github.com/{owner}/{name}.git
    repo_name - name of repository in github.com/{owner}/{name}.git
    repo_dir - where to checkout our repo, prior to building commits
               (default: /tmp/nextli-datasette)

## Usage

The plugin adds an interface at `/-/git-importer` for uploading a CSV file, setting meta configuration and pushing a commit to a specified repo.

## Development

There's two parts to this plugin: a Preact app that builds the datasette template and the python backend code.

If you don't want to mess with the frontend UI, just install the plugin like described above. If you do
want to edit the UI, the Preact app is in `config-ed`. To build the component and update the datasette template,
run `npm run build`. This will run the entire JS build process and will update the template file and static
assets. Re-installing the plugin will push the changes to datasette.
