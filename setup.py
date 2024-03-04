"""
This script performs version-related tasks for chart directories based on Git changes.
"""

from setuptools import setup

setup(
    name='bump-helm-chart-version',
    version='1.1.4',
    description='Bump helm chart version if the /templates folder has changes',
    author='Youssef Hussein',
    author_email='youssef@doubl.tech',
    packages=['bump_helm_chart_version'],
    install_requires=['PyYAML'],
    entry_points={
        'console_scripts': [
            'bump-chart-version = bump_helm_chart_version.bump_chart_version:main',
        ],
    },
    include_package_data=True,
)
