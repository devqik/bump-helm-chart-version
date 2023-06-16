from setuptools import setup

setup(
    name='bump-helm-chart-version',
    version='1.0.0',
    description='Pre-commit hook for bumping Helm chart versions',
    author='Your Name',
    author_email='your@email.com',
    packages=['bump_helm_chart_version'],
    install_requires=['pyyaml'],
    entry_points={
        'console_scripts': [
            'bump-chart-version = bump_helm_chart_version.bump_chart_version:main',
        ],
    },
)
