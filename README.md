# Webshell Analyzer
webshell analyzer is command line based webshell detection tool that utillizes static feature extraction and using Random Forest classification to detect malicious PHP webshell.

![Webshell Analyzer Home Screen](/assets/images/home_screen.png "Home Screen")

## Table of Contens
- [About](#about)
- [Features](#features)
- [Requirements](#requirements)
- [Instalation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Example Output](#example-output)

## About
webshell analyzer was developed to assist security analysts, researchers, and system administrators in identifying potentially malicious PHP files before they are executed on a web server. the tool helps to mitigate the risk of unauthorised access, web defacement attacks, and persistent backdoor attacks, which are commonly associated with webshells.

this system combines three static code analysis methods: lexical analysis, statistical analysis, and Abstract Syntax Tree (AST) analysis. this approach enables the detection process to identify suspicious functions, code structure patterns, and statistical characteristics that may indicate malicious behavior.

## Features
- Scan individual PHP files for webshell indicators
- Recursively scan entire directories
- Static feature extraction (no code execution required)
- Machine learning classification using Random Forest
- Export results to only JSON file
- Interactive CLI environment

## Requirements
before installing and running webshell analyzer, ensure that your system meets the following requirements :

- Python 3.10 or later
- Pip (python package manager)
- Git

## Installation
to install webshell analyzer, clone this repository to your local machine using the following command :

```git clone https://github.com/Adeliasaputriiii/webshell-analyzer```

After the installation process is complete, the system is ready to use.

## Usage
Use the following command to launch the webshell analyzer interactive environment :

```wsanalyzer```

once started, you will be presented with the webshell analyzer command prompt. From this environment, you can run all available commands such as `scan`, `detect`, `--output`, `help`, `exit`.

## Commands
1. ```scan <directory_path> [--output <output_file.json>]``` -> scan all PHP files in a directory for webshell detection
2. ```detect <file_path> [--output <output_file.json>]``` -> detect a specific file for webshell activity
3. ```help``` -> for show this help message
4. ```exit``` -> For Exit the Webshell Analyzer
5. ```--output <output_file.json>``` -> Save the detection results to a JSON file

## Example Output
![Process Detecting Single file PHP](/assets/images/detectFile.png "detecting File")
