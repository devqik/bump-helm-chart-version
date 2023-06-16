from setuptools import setup

setup(
    name='bump-helm-chart-version',
    version='1.0.0',
    description='Bump helm chart version if the /templates folder has changes',
    author='Youssef Hussein',
    author_email='youssef@doubl.tech',
    packages=['bump_helm_chart_version'],
    install_requires=['pyyaml'],
    entry_points={
        'console_scripts': [
            'bump-chart-version = bump_helm_chart_version.bump_chart_version:main',
        ],
    },
)
