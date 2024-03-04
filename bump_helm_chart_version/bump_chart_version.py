#!/usr/bin/env python3

"""
This script performs version-related tasks for chart directories based on Git changes.
"""

import subprocess
import sys
import os
import yaml

def main():
    """
    Main function for performing version-related tasks on chart directories.
    """

    def increment_patch_version(version):
        """
        Increment the patch version of a given version string.
        """
        parts = version.split('.')
        if len(parts) != 3:
            raise ValueError(f'Invalid version string: {version}')
        try:
            patch = int(parts[2])
        except ValueError as exc:
            raise ValueError(f'Invalid patch version: {parts[2]}') from exc
        new_patch = patch + 1
        new_version = f'{parts[0]}.{parts[1]}.{new_patch}'
        return new_version

    # Retrieve main branch name
    main_branch_name = next(
        line.split(':')[1].strip()
        for line in subprocess.check_output(['git', 'remote', 'show', 'origin'],
            text=True).split('\n')
        if line.startswith('  HEAD branch:')
    )


    print(main_branch_name)  # Output the main branch name

    # Get list of chart directories that have changed
    git_diff_output = subprocess.run(
        ['git', 'diff', '--name-only', main_branch_name],
        check=True, capture_output=True, text=True
    )
    changed_files = git_diff_output.stdout.splitlines()

    chart_dirs = list(dict.fromkeys(
        os.path.join(*parts[:-1]) if parts[-1] == 'templates' else os.path.join(*parts)
        for file in changed_files
        for parts in [os.path.split(os.path.dirname(file))]
        if file.endswith('.yaml') or '/templates' in file
    ))

    print("Changed chart directories: ", chart_dirs)

    for chart_dir in chart_dirs:
        if not os.path.exists(f'{chart_dir}/Chart.yaml'):
            print(f"Skipping {chart_dir} because it does not contain a Chart.yaml file")
            continue

        # Get versions
        prev_version = yaml.safe_load(
            subprocess.run(['git', 'show', f'{main_branch_name}:{chart_dir}/Chart.yaml'],
                        check=True, capture_output=True, text=True).stdout
        )['version']

        with open(f'{chart_dir}/Chart.yaml', 'r', encoding='utf-8') as chart_yaml_file:
            current_version = next(
                line.split()[1].strip()
                for line in chart_yaml_file
                if line.startswith('version:')
            )

        new_version = increment_patch_version(prev_version)
        # Echo previous and current versions
        print(f"The previous version is {prev_version}")
        print(f"The current version is {current_version}")

        # Check if Chart version was changed manually
        if prev_version != current_version:
            print("Chart was updated")
        else:
            print(f"Checking chart version in {chart_dir}")
            if new_version != current_version:
                print(f"Updating chart version from {current_version} to {new_version}")
                with open(f'{chart_dir}/Chart.yaml', 'r+', encoding='utf-8') as chart_yaml_file:
                    lines = chart_yaml_file.readlines()
                    chart_yaml_file.seek(0)
                    chart_yaml_file.truncate()
                    for line in lines:
                        if line.startswith('version:'):
                            chart_yaml_file.write(f'version: {new_version}\n')
                        else:
                            chart_yaml_file.write(line)
                subprocess.run(['git', 'add', f'{chart_dir}/Chart.yaml'], check=True)

if __name__ == '__main__':
    sys.exit(main())
