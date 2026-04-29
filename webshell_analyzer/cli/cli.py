import pyfiglet
import cmd
import os
import shlex
import json
import sys
from colorama import Fore, Style, init
from webshell_analyzer.modules.detector import detect_file
from webshell_analyzer.modules.scanner import scan_directory

sys.stdout.reconfigure(encoding='utf-8')
init(autoreset=True)

def banner ():
    f = pyfiglet.figlet_format("W3bshell-Analyzer", font="big_money-se")
    print(Fore.MAGENTA + f)
    print(Fore.MAGENTA + "Webshell Analyzer Tool Integrating Machine Learning".center(80))
    print(Fore.MAGENTA + "Based on Extracting Features from PHP Source Code".center(80))
    print(Fore.MAGENTA + "=" * 80)
    print(Fore.MAGENTA + "Author : Adelia Saputri")
    print(Fore.MAGENTA + "Github : https://github.com/adeliasaputri")
    print(Fore.MAGENTA + "Email  : adeliasaputri@example.com")
    print(Fore.MAGENTA + "Engine : AST + Lexical + Statistical Features")
    print(Fore.MAGENTA + "=" * 80 + "\n")

def parse_args(args):
    path = None
    output = None

    i = 0
    while i < len(args):
        if args[i] == "--output":
            if i + 1 < len(args):
                output = args[i + 1]
                i += 1
        else:
            path = args[i]
        i += 1
    return path, output

class webshell_cmd(cmd.Cmd):
    prompt = Fore.MAGENTA + "w3bshell-analyzer> "

    def do_scan(self, arg):
        """Scan Directory: scan <directory_path>"""
        try :
            args = shlex.split(arg)
        except :
            print(Fore.RED + "Error: Invalid arguments. Usage: scan <path> [--output <output_file>]\n")
            return
        
        if len(args) == 0:
            print(Fore.RED + "[ERROR] Path is required. Usage: scan <path> [--output <output_file>]\n")
            return
        
        directorypath, output = parse_args(args)

        if not os.path.isdir(directorypath):
            print(Fore.RED + f"[ERROR] Path '{directorypath}' is not a valid directory.\n")
            return
        print(Fore.GREEN + f"[SCANNING DIRECTORY..]: {directorypath}\n")

        result = scan_directory(directorypath, output_file=output)
    
    def do_detect(self, arg):
        """Detect File: detect <file_path>"""
        try :
            args = shlex.split(arg)
        except :
            print(Fore.RED + "[ERROR] Invalid arguments. Usage: detect <file_path> [--output <output_file>]\n")
            return
        
        if len(args) == 0:
            print(Fore.RED + "[ERROR] Path is required. Usage: detect <path> [--output <output_file>]\n")
            return
        
        filepath, output = parse_args(args)

        if not os.path.isfile(filepath):
            print(Fore.RED + f"[ERROR] File '{filepath}' does not exist.\n")
            return
        
        print (Fore.GREEN + f"[ANALYZING..] {filepath}")
        detect_file(filepath, output_file=output)


    def do_help(self, arg):
        """Show help message"""
        print(Fore.CYAN + "=" * 50 + "\n")
        print(Fore.CYAN + "Available commands: ")
        print(Fore.CYAN + "scan <directory_path> -> for scan a directory for webshell")
        print(Fore.CYAN + "detect <file_path> -> for detect if a specific file is a webshell")
        print(Fore.CYAN + "help -> for show this help message")
        print(Fore.CYAN + "exit -> For Exit the Webshell Analyzer")
        print(Fore.CYAN + "=" * 50 + "\n")

    def do_exit(self, arg):
        """Exit the webshell analyzer"""
        print(Fore.GREEN + "Exiting webshell analyzer, Goodbye!\n")
        return True
    
    def default(self, line):
        """Handle unknown commands"""
        print(Fore.RED +  "Unknown command: " + f'{line}')
        print("Type 'help' for a list of available commands.\n")

def main() :
    banner()
    webshell_cmd().cmdloop()

if __name__ == "__main__":
    main()

