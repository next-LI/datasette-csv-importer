from setuptools import setup
import os

VERSION = "1.0.4"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-csv-importer",
    description="Datasette plugin for live-uploading CSV files with a user-friendly configuration UI.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Brandon Roberts <brandon@bxroberts.org>",
    url="https://github.com/next-LI/datasette",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_csv_importer"],
    entry_points={"datasette": ["csv_importer = datasette_csv_importer"]},
    install_requires=[
        # "datasette>=0.51",
        "asgi-csrf>=0.7",
        "starlette",
        "aiofiles",
        "python-multipart",
        "sqlite-utils",
        "csvs-to-sqlite>=1.2,<1.3.0",
        "GitPython>=3.1.15,<3.2",
    ],
    extras_require={
        "test": ["pytest", "pytest-asyncio"]
    },
    package_data={"datasette_csv_importer": [
        "static/*",
        "static/jsonform/deps/underscore.js",
        "static/jsonform/deps/jquery.min.js",
        "static/jsonform/deps/opt/*",
        "static/jsonform/lib/*.js",
        "templates/*"
    ]},
    tests_require=["datasette-csv-importer[test]"],
)
