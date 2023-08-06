# hypermodern-python-cli99

[![Tests](https://github.com/cli99/hypermodern-python-cli99/workflows/Tests/badge.svg)](https://github.com/cli99/hypermodern-python-cli99/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/cli99/hypermodern-python-cli99/branch/master/graph/badge.svg)](https://codecov.io/gh/cli99/hypermodern-python-cli99)
[![PyPI](https://img.shields.io/pypi/v/hypermodern-python-cli99.svg)](https://pypi.org/project/hypermodern-python-cli99/)
[![Read the Docs](https://readthedocs.org/projects/hypermodern-python-cli99/badge/)](https://hypermodern-python-cli99.readthedocs.io/)

https://github.com/cjolowicz/hypermodern-python

https://cjolowicz.github.io/posts/hypermodern-python-01-setup/

> **_NOTE:_** this package does not publish to PyPI due to the package name conflict, the badge shows the original package.

## Use Poetry to manage Black, Flake8, and the other tools as development dependencies

```
poetry add --dev \
    black \
    flake8 \
    flake8-bandit \
    flake8-black \
    flake8-bugbear \
    flake8-import-order \
    safety
```

## Use pre-commit

```
pip install --user --upgrade pre-commit
```

## Use xdoctest to run documentation exmamples

```
poetry add --dev xdoctest
```

## Create documenation with Sphinx

```
poetry add --dev sphinx
```
