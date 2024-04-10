<p align="center">
    <img alt="batchee, a python package for grouping together filenames to enable subsequent batched operations (such as concatenation)."
    src="https://github.com/danielfromearth/batchee/assets/114174502/8b1a92a5-eccc-4674-9c00-3698e752077e" width="250"
    />
</p>

<p align="center">
    <a href="https://www.repostatus.org/#active" target="_blank">
        <img src="https://www.repostatus.org/badges/latest/active.svg" alt="Project Status: Active – The project has reached a stable, usable state and is being actively developed">
    </a>
    <a href="https://github.com/python/black" target="_blank">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style">
    </a>
    <a href="http://mypy-lang.org/" target="_blank">
        <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Mypy checked">
    </a>
</p>

[//]: # (Using deprecated `align="center"` for the logo image and badges above, because of https://stackoverflow.com/a/62383408)


# Overview
_____

_Batchee_ groups together filenames so that further operations (such as concatenation) can be performed separately on each group of files.

## Installing
_____

For local development, one can clone the repository and then use poetry or pip from the local directory:

```shell
git clone <Repository URL>
```

###### (Option A) using poetry:
i) Follow the instructions for installing `poetry` [here](https://python-poetry.org/docs/).

ii) Run ```poetry install``` from the repository directory.

###### (Option B) using pip: Run ```pip install .``` from the repository directory.

## Usage
_____

```shell
batchee [file_names ...]
```

###### Or, If installed using a `poetry` environment:
```shell
poetry run batchee [file_names ...]
```

#### Options

- `-h`, `--help`            show this help message and exit
- `-v`, `--verbose`  Enable verbose output to stdout; useful for debugging

---
This package is NASA Software Release Authorization (SRA) # LAR-20440-1
