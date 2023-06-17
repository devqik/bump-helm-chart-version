#!/usr/bin/env python3

import os
import subprocess
import sys

# Check if required packages are installed and install them if necessary
try:
    import yaml
except ImportError:
    subprocess.run(['pip', 'install', 'pyyaml'], check=True)
    import yaml

def main(argv=None):

    def increment_patch_version(version):
        parts = version.split('.')
        if len(parts) != 3:
            raise ValueError('Invalid version string: {}'.format(version))
        try:
            patch = int(parts[2])
        except ValueError:
            raise ValueError('Invalid patch version: {}'.format(parts[2]))
        new_patch = patch + 1
        new_version = '{}.{}.{}'.format(parts[0], parts[1], new_patch)
        return new_version

    # Run git command to retrieve main branch name
    git_show_remote_command = ['git', 'remote', 'show', 'origin']
    git_show_remote_command_output = subprocess.check_output(git_show_remote_command, text=True)

    # Parse output to extract main branch name
    lines = git_show_remote_command_output.split('\n')
    for line in lines:
        if line.startswith('  HEAD branch:'):
            main_branch_name = line.split(':')[1].strip()
            break  # Corrected indentation

    print(main_branch_name)  # Output the main branch name

    # Get list of chart directories that have changed
    git_diff_output = subprocess.run(['git', 'diff', '--name-only', 'HEAD'], check=True, capture_output=True, text=True)
    changed_files = [filename for filename in git_diff_output.stdout.splitlines()]

    chart_dirs = [os.path.dirname(file) for file in changed_files if file.endswith('/Chart.yaml') or '/templates' in file]
    chart_dirs = [os.path.split(dir_path) for dir_path in chart_dirs]
    chart_dirs = [os.path.join(*parts[:-1]) if parts[-1] == 'templates' else os.path.join(*parts) for parts in chart_dirs]
    chart_dirs = list(dict.fromkeys(chart_dirs))

    for chart_dir in chart_dirs:
        # Get versions
        prev_version_chart_file = subprocess.run(['git', 'show', f'{main_branch_name}:{chart_dir}/Chart.yaml'], check=True, capture_output=True, text=True).stdout
        prev_version_dict = yaml.safe_load(prev_version_chart_file)
        prev_version = prev_version_dict['version']
        with open(f'{chart_dir}/Chart.yaml', 'r') as f:
            current_version = [line.split()[1] for line in f.readlines() if line.startswith('version:')][0].strip()

        new_version = increment_patch_version(prev_version)
        # Echo previous and current versions
        print(f"The previous version is {prev_version}")
        print(f"The current version is {current_version}")

        # Check if Chart version was changed manually
        if prev_version == current_version:
            print(f"Checking chart version in {chart_dir}")
            if new_version != current_version:
                print(f"Updating chart version from {current_version} to {new_version}")
                with open(f'{chart_dir}/Chart.yaml', 'r+') as f:
                    lines = f.readlines()
                    f.seek(0)
                    f.truncate()
                    for line in lines:
                        if line.startswith('version:'):
                            f.write(f'version: {new_version}\n')
                        else:
                            f.write(line)
                subprocess.run(['git', 'add', f'{chart_dir}/Chart.yaml'], check=True)
        else:
            print("Chart was updated")

if __name__ == '__main__':
    sys.exit(main())
