import pyfiglet
import cmd
import os
from colorama import init, Fore, Style
from modules.scanner import scan_directory
from modules.detector import processing_file

init(autoreset=True)

def banner ():
    f = pyfiglet.figlet_format("Webshell-Detector", font="big_money-se")
    print(Fore.GREEN + f)
    print(Fore.GREEN + "Webshell Detection Tool integrating Machine Learning".center(80))
    print(Fore.GREEN + "Based on Extracting Features from PHP Sources Code".center(80))
    print(Fore.GREEN + "=" * 80)
    print(Fore.GREEN + " Author  : Adelia saputri")
    print(Fore.GREEN + " Version : 1.0")
    print(Fore.GREEN + " Engine  : AST + Lexical + Statistical Features")
    print(Fore.GREEN + "=" * 80 + "\n")

class webshell_cmd(cmd.Cmd):
    prompt = Fore.GREEN + "webshell-detector> " + Style.RESET_ALL

    def do_scan(self, arg):
        """Scan directory: scan <directory_path>"""
        directorypath = arg.strip()
        if not directorypath:
            print(Fore.RED + "Usage: scan <directory_path>")
            return
        if not os.path.isdir(directorypath):
            print(Fore.RED + f"[ERROR] Directory '{directorypath}' does not exist.")
            return
        
        print(Fore.GREEN + f"[SCAN] " + f"{directorypath}")
        scan_directory(directorypath)
    
    def do_detect(self, arg):
        """Detect file: detect <file_path>"""
        filepath = arg.strip()
        if not filepath:
            print(Fore.RED + "Usage: detect <file_path>")
            return
        if not os.path.isfile(filepath):
            print(Fore.RED + f"[ERROR] File '{filepath}' does not exist.")
            return
     
        print (Fore.GREEN + f"[DETECT] " + f"{filepath}")
        processing_file(filepath)
    

    def do_help(self, arg):
        """Show help message"""
        print(Fore.CYAN + "Available commands:")
        print(Fore.CYAN + "  scan <directory_path> - Scan a directory for webshells")
        print(Fore.CYAN + "  detect <file_path> - Detect if a specific file is a webshell")
        print(Fore.CYAN + "  help - Show this help message")
        print(Fore.CYAN + "  exit - Exit the Webshell Detector")
    
    def do_exit(self, arg):
        """Exit the Webshell Detector"""
        print(Fore.GREEN + "Exiting Webshell Detector, Goodbye!")
        return True
    
    def default(self, line):
        """Handle unknown commands"""
        print(Fore.RED + "Unknown command: " + f'{line}')
        print("Type 'help' for a list of available commands.")

def main() :
    banner()
    webshell_cmd().cmdloop()

if __name__ == "__main__":
    main()