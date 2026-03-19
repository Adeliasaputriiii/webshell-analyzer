import os 
from webshell_detector.modules.detector import processing_file

def scan_directory(directorypath):
    
    
    total_files = 0
    total_processed_files = 0
    total_webshells = 0

    results = []

    print(f"[SCAN] Scanning directory: {directorypath}\n")

    for root, dirs, files in os.walk(directorypath):
        for file in files:
            filepath = os.path.join(root, file)
            total_files += 1

            result = processing_file(filepath)

            if result is not None:
                total_processed_files += 1
                results.append((filepath, result))
                print(f"[{result.upper()}] {filepath}\n")

                if result.lower() == "webshell":
                    total_webshells += 1

    print(f"=====SCAN SUMMARY=====\n")
    print(f"Total files: {total_files}\n")
    print(f"Processed files: {total_processed_files}\n")
    print(f"Webshells found: {total_webshells}\n")

    return results


