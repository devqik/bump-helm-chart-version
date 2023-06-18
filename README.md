# bump-helm-chart-version Pre-commit Hook

## Overview

bump-helm-chart-version is a pre-commit hook written in Python 3. It requires pyyaml to be installed and is used to automatically bump the Helm chart patch version if the chart has changes in the `/templates` folder or changes in helper functions files.

## Usage

Installation
To use this pre-commit hook, you must first install the pre-commit framework. Follow the instructions provided in the pre-commit documentation.

Once pre-commit is installed, add the following to your .pre-commit-config.yaml file:

``` yaml
repos:
  - repo: https://github.com/devqik/bump-helm-chart-version
    rev: v1.0.6
    hooks:
      - id: bump-chart-version
        entry: bump-chart-version
        language: python
        name: Bump chart version
```

## Configuration

This pre-commit hook looks for changes in the /templates folder and helper function files to determine if the Helm chart patch version should be bumped. If you need to change the directory, main branch name or file pattern, you can modify the bump_chart_version.py script.

## Execution

After adding the configuration to your .pre-commit-config.yaml file, the pre-commit hook will automatically run on git commit. If the pre-commit hook detects that the Helm chart version needs to be bumped, it will modify the version field in the Chart.yaml file.

## Contributing

Contributions are welcome! Please follow the contributing guidelines when making changes to this repository.

## License

This pre-commit hook is licensed under the BSD 3-Clause License.
