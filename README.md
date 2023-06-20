# bump-helm-chart-version Pre-commit Hook

## Overview

bump-helm-chart-version is a pre-commit hook written in Python 3. It requires pyyaml to be installed and is used to automatically bump the Helm chart patch version if the chart has changes in the `/templates` folder or changes in helper functions files.

## Features

- Automatically increments the patch version of a Helm chart
- Integrates seamlessly with pre-commit hooks

## Installation

To use bump-helm-chart-version, follow these steps:

- Ensure Python 3 is installed on your system.

- Configure the pre-commit hook in your repository's .pre-commit-config.yaml file:

```yaml
repos:
  - repo: https://github.com/devqik/bump-helm-chart-version
    rev: v1.1.0
    hooks:
      - id: bump-chart-version
        entry: bump-chart-version
        language: python
        name: Bump chart version
``` 

- Install the pre-commit hook by running:

```script
pre-commit install
```

## Usage

Once the pre-commit hook is installed, it will automatically run whenever you make changes to files in the /templates folder or the helper function files of your Helm chart. If changes are detected, the patch version of the chart will be incremented.

## Contributions

Contributions are welcome! If you find a bug or want to suggest an enhancement, please open an issue or submit a pull request.

## License

This pre-commit hook is licensed under the BSD 3-Clause License.
