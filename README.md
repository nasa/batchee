<p align="center">
    <img alt="Batchee logo"
    src="https://github.com/danielfromearth/batchee/assets/114174502/8b1a92a5-eccc-4674-9c00-3698e752077e" width="250"
    />
</p>

<p align="center">
    <a href="https://www.repostatus.org/#active" target="_blank">
        <img src="https://www.repostatus.org/badges/latest/active.svg" alt="Project Status: Active – The project has reached a stable, usable state and is being actively developed">
    </a>
    <a href="https://mypy-lang.org/" target="_blank">
        <img src="https://www.mypy-lang.org/static/mypy_badge.svg" alt="Mypy checked">
    </a>
    <a href="https://pypi.org/project/batchee/" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/batchee.svg" alt="Python Versions">
    </a>
    <a href="https://pypi.org/project/batchee" target="_blank">
        <img src="https://img.shields.io/pypi/v/batchee?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
    <a href="https://codecov.io/gh/nasa/batchee">
     <img src="https://codecov.io/gh/nasa/batchee/graph/badge.svg?token=WDj92iN7c4" alt="Code coverage">
    </a>
</p>

[//]: # (Using deprecated `align="center"` for the logo image and badges above, because of https://stackoverflow.com/a/62383408)


# Overview

**Batchee** is a Python package that intelligently groups filenames together, enabling efficient batch operations like concatenation.

### What does it do?

Batchee analyzes filename patterns and groups related files together.
For example (_note that these are pseudo-real, not actual, TEMPO file names_):

```shell
batchee TEMPO_NO2_L2_S006G01.nc TEMPO_NO2_L2_S006G02.nc TEMPO_NO2_L2_S007G08.nc TEMPO_NO2_L2_S007G09.nc
```

**Output:**
- `TEMPO_NO2_L2_S006G01.nc`, `TEMPO_NO2_L2_S006G02.nc` → Group 1 (scan 6)
- `TEMPO_NO2_L2_S007G08.nc`, `TEMPO_NO2_L2_S007G09.nc` → Group 2 (scan 7)

This enables batch processing operations on each group separately.

### Key Features
- Automatic filename grouping based on configurable patterns
- Command-line interface and Python API for integration with NASA Harmony service orchestrator
- Verbose logging for debugging

## Installation

### From PyPI (Recommended)
```shell
pip install batchee
```

### From Source (Development)

For local development or the latest features:

```shell
git clone <Repository URL>
cd batchee
```

**(Option A) using poetry (Recommended for development):**

```shell
# Install poetry: https://python-poetry.org/docs/
poetry install
```

**(Option B) using pip:**

```shell
pip install .
```

## Usage

### Basic Usage

```shell
batchee [file_names ...]
```

### With Poetry (if installed via poetry)
```shell
poetry run batchee [file_names ...]
```

### Options

- **`-h, --help`** - Show help message and exit
- **`-v, --verbose`** - Enable verbose output to stdout; useful for debugging

## Contributing

Issues and pull requests welcome on [GitHub](https://github.com/nasa/batchee/).

## License & Attribution

Batchee is released under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

This package is NASA Software Release Authorization (SRA) # LAR-20440-1
