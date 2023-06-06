# Development

## Prerequisites

Better use UNIX.

Install [Python 3.7+](https://www.python.org/downloads/).

Install [Poetry](https://python-poetry.org/docs/#installation).

Install dependencies:

```bash
make install
```

Install [LilyPond](http://lilypond.org/download.html).

Setup pre-commit hooks:

```bash
make setup-pre-commit-hooks
```

## Makefile utilities


```bash
make help
```

``` 
Usage: make <target>

Targets:
  help                      Show help.
  install                   Install dependencies.
  setup-pre-commit-hooks    Setup pre-commit hooks.
  run                       Run CLI.
  dev                       Run CLI in a dev mode.
  build                     Build binaries for different systems.
  test                      Test project.
  lint                      Lint project code.
  format                    Format project code.
  release                   Create a new tag for release.
  docs-start                Start documentation local web server.
  docs-build                Build documentation.
  docs-deploy               Deploy documentation build.
  clean                     Clean ignored files.
  export-dependencies       Export dependencies into requirements.txt.
  env-info                  Display virtual environment and system information.
```

## Troubleshoots

### CV2 autocomplete doesn't work in my IDE

Issue: https://stackoverflow.com/questions/73174194/opencv-autocomplete-not-working-on-pycharm
Workaround: https://stackoverflow.com/a/75054982
