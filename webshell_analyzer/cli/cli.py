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
    print(Fore.MAGENTA + "Email  : adelias.dev@gmail.com")
    print(Fore.MAGENTA + "Engine : AST + Lexical + Statistical Features")
    print(Fore.MAGENTA + "=" * 80 + "\n")

def parse_args(args):
    path = None
    output = None
    output_missing = False

    i = 0
    while i < len(args):
        if args[i] == "--output":
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                output = args[i + 1]
                i += 1
            else:
                output_missing = True
        else:
            path = args[i]
        i += 1
    return path, output, output_missing

class webshell_cmd(cmd.Cmd):
    prompt = Fore.MAGENTA + "w3bshell-analyzer> "

    def do_scan(self, arg):
        """Scan Directory: scan <directory_path>"""
        try :
            args = shlex.split(arg)
        except :
            print(Fore.RED + "Error: Invalid arguments. Usage: scan <path> [--output <output_file>]")
            return
        
        if len(args) == 0:
            print(Fore.RED + "[ERROR] Path is required. Usage: scan <path> [--output <output_file>]")
            return
        
        directorypath, output, output_missing = parse_args(args)

        if output_missing:
            print(Fore.RED + "[ERROR] flag '--output' is requires a filename argument. Usage: detect <file_path> --output <output_file.json>")
            return

        if not os.path.isdir(directorypath):
            print(Fore.RED + f"[ERROR] Path '{directorypath}' is not a valid directory.")
            return
        
        #Validasi output
        if output is not None:
            output_dir = os.path.dirname(output)
            if output_dir != "" and not os.path.isdir(output_dir):
                print(Fore.RED + f"[ERROR] Cannot save output to Directory \"{output_dir}\". Please ensure the destination folder exists before saving!")
                return
            if not output.endswith(".json"):
                print(Fore.RED + f"[ERROR] Output file must have a .json extension")
                return

        print(Fore.GREEN + f"[SCANNING DIRECTORY..]: {directorypath}\n")
        result = scan_directory(directorypath, output_file=output)
    
    def do_detect(self, arg):
        """Detect File: detect <file_path>"""
        try :
            args = shlex.split(arg)
        except :
            print(Fore.RED + "[ERROR] Invalid arguments. Usage: detect <file_path> [--output <output_file>]")
            return
        
        if len(args) == 0:
            print(Fore.RED + "[ERROR] Path is required. Usage: detect <path> [--output <output_file>]")
            return
        
        filepath, output, output_missing = parse_args(args)

        if output_missing:
            print(Fore.RED + "[ERROR] flag '--output' is requires a filename argument. Usage: detect <file_path> --output <output_file.json>")
            return

        if not os.path.isfile(filepath):
            print(Fore.RED + f"[ERROR] File '{filepath}' does not exist.")
            return

        #Validasi output
        if output is not None:
            output_dir = os.path.dirname(output)
            if output_dir != "" and not os.path.isdir(output_dir):
                print(Fore.RED + f"[ERROR] Cannot save output to Directory {output_dir}")
                print(Fore.RED + f"Please ensure the destination folder exists before saving")
                return
            if not output.endswith(".json"):
                print(Fore.RED + f"[ERROR] Output file must have a .json extension")
                return
        
        print (Fore.GREEN + f"[ANALYZING..] {filepath}")
        detect_file(filepath, output_file=output)


    def do_help(self, arg):
        """Show help message"""
        print(Fore.CYAN + "=" * 50)
        print(Fore.CYAN + "AVAILABLE COMMANDS: \n")
        print(Fore.CYAN + "scan <directory_path> [--output <output_file.json>] -> scan all PHP files in a directory for webshell detection")
        print(Fore.CYAN + "detect <file_path> [--output <output_file.json>] -> detect a specific file for webshell activity")
        print(Fore.CYAN + "help -> for show this help message")
        print(Fore.CYAN + "exit -> For Exit the Webshell Analyzer")
        print(Fore.CYAN + "=" * 50)
        print(Fore.CYAN + "OPTIONAL ARGUMENTS: \n")
        print(Fore.CYAN + "--output <output_file.json> -> Save the detection results to a JSON file")
        print(Fore.CYAN + "=" * 50 + "\n")

    def do_exit(self, arg):
        """Exit the webshell analyzer"""
        print(Fore.GREEN + "Exiting webshell analyzer, Goodbye!")
        return True
    
    def default(self, line):
        """Handle unknown commands"""
        print(Fore.RED +  "Unknown command: " + f'{line}')
        print("Type 'help' for a list of available commands.\n")

    def emptyline(self):
        pass

def main() :
    banner()
    webshell_cmd().cmdloop()

if __name__ == "__main__":
    main()

