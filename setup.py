from setuptools import setup
import os

VERSION = "0.6"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-git-importer",
    description="Datasette plugin for uploading CSV files, editing configuration and creating commits representing the changes.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/next-LI/datasette",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_git_importer"],
    entry_points={"datasette": ["git_importer = datasette_git_importer"]},
    install_requires=[
        "datasette>=0.51",
        "asgi-csrf>=0.7",
        "starlette",
        "aiofiles",
        "python-multipart",
        "sqlite-utils",
        "requests",
        "GitPython>=3.1.14,<4.0",
    ],
    extras_require={
        "test": ["pytest", "pytest-asyncio", "asgiref", "httpx", "asgi-lifespan"]
    },
    package_data={"datasette_git_importer": ["static/*", "templates/*.html"]},
)
