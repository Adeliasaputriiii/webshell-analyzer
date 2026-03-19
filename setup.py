from setuptools import setup, find_packages

setup(
    name='webshell_detector',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pyfiglet',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'webshdet=webshell_detector.cli.cli:main',
        ]
    }
)
