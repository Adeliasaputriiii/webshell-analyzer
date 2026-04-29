from setuptools import setup, find_packages

setup(
    name='webshell_analyzer',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pyfiglet',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'wsanalyzer=webshell_analyzer.cli.cli:main',
        ]
    }
)
