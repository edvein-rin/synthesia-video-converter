# Development

## Prerequisites

Better use UNIX.

Install [Python 3.7+](https://www.python.org/downloads/).

Install [Poetry](https://python-poetry.org/docs/#installation).

Install dependencies:

```bash
make install
```

## Makefile utilities


```bash
make help
```

``` 
Usage: make <target>

Targets:
  help                      Show the help.
  install                   Install dependencies.
  run                       Run the project.
  test                      Test the project.
  lint                      Lint the project code.
  format                    Format the project code.
  build                     Build the project.
  release                   Create a new tag for release.
  docs-start                Start documentation local web server.
  docs-build                Build documentation.
  docs-deploy               Deploy documentation build.
  env-info                  Display virtual environment and system information.
```
