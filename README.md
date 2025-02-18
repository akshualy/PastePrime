# PastePrime

A tool to paste clipboard contents one key at a time.
Bypasses the Warframe bug that prevents using Ctrl + V.

## Requirements

For development, you need at least

- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

## Installing

After installing poetry, you can open a command line with the project as the working directory and run

```commandline
poetry install --with dev
```

## Running

It is possible to run the project with

```commandline
python main.py
```

But I recommend bundling to an exe with

```commandline
pyinstaller PastePrime.exe
```

The exe allows auto-starting it with Windows.

## Caveats

For now, only Windows is supported for auto-starting.

## Contributing

Any contribution is welcome. However, the project uses automatic linting tools.  
Please run these commands before opening a pull request:

```commandline
black .
isort .
flake8
```
