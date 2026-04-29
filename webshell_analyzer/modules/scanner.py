import os
import sys 
from colorama import Style, Fore
import json
from webshell_analyzer.modules.detector import processing_file

def scan_directory(directorypath, output_file=None):
    
    total_files = 0
    total_processed_files = 0
    total_filewebshells = 0
    total_filenormal = 0

    results = []

    for root, _, files in os.walk(directorypath):
        for file in files:
            filepath = os.path.join(root, file)
            total_files += 1
            
            result = processing_file(filepath)
            
            results.append(result)

            if result["status"] == "processed":
                print(Fore.GREEN + f"[{result['prediction'].upper()}] {filepath}")
                total_processed_files += 1
                
                if result["prediction"].lower() == "webshell":
                    total_filewebshells += 1
                else :
                    total_filenormal += 1
            else:
                print(Fore.YELLOW + f"[SKIPPED] {filepath}")

    summary = {
        "total files": total_files,
        "processed_files": total_processed_files,
        "skipped files": total_files - total_processed_files,
        "normal files": total_filenormal,
        "webshell files": total_filewebshells
    }

    final_output = {
        "results" : results,
        "summary": summary
    }

    if output_file:
        with open(output_file, "w") as f:
            json.dump(final_output, f, indent=4)
        print(Fore.GREEN + f"Result Saved to {output_file}")

    print(Fore.GREEN + "\n" + "=" * 50)
    print(Fore.GREEN + "SCAN SUMMARY".center(50))
    print(Fore.GREEN + "=" * 50)
    print(Fore.GREEN + f"Total files: {total_files}")
    print(Fore.GREEN + f"Processed files: {total_processed_files}")
    print(Fore.GREEN + f"Skipped files: {total_files - total_processed_files}")
    print(Fore.GREEN + f"normal files: {total_filenormal}")
    print(Fore.GREEN + f"webshell files: {total_filewebshells}")
    print(Fore.GREEN + "=" * 50 + "\n")

    sys.stdout.write(Style.RESET_ALL)
    sys.stdout.flush()

    return output_file, results


