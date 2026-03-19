import os

php_extensions = ['.php', '.phtml', '.php3', '.php4', '.php5', '.phps']
max_file_size = 10_000_000  # 10 MB

def check_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read(2000)
        if "<?php" in content or "<?=" in content:
            return True
        else:
            return False
    except Exception as e:
        print(f"[ERROR] Could not read file '{filepath}': {e}")
        return False

def is_php_file(filepath): 
    size = os.path.getsize(filepath)

    if size <= max_file_size:
        if filepath.lower().endswith(tuple(php_extensions)):
            return True
    
        return check_file_content(filepath)
    else :
        print(f"[ERROR] File '{filepath}' exceeds the maximum allowed size of {max_file_size} bytes.")
        return False
    
def processing_file(filepath):

    if not is_php_file(filepath):
        print(f"[ERROR] File '{filepath}' is not a PHP file.")
        return None
    
    print (f"[PROCESS] {filepath}")

    #ekstraksi
    #features = extract_features(filepath)
    #result = model.predict(features)

    #if result is None:
    # print ("File not found or not a valid PHP file.")
    # continue;

    #return result

    