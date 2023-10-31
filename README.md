[<img src="https://github.com/danielfromearth/batchee/assets/114174502/8b1a92a5-eccc-4674-9c00-3698e752077e" width="250"/>](stitchee_9_hex)


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
