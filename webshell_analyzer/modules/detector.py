import os
import sys
import json
from colorama import Fore, Style
import pandas as pd
from webshell_analyzer.extractor.extractor import extract_features
from webshell_analyzer.model.model_loader import load_feature_columns, load_model

feature_columns = load_feature_columns()
model = load_model()

php_extensions = ['.php', '.phtml', '.php3', '.php4', '.php5', '.phps']
max_file_size = 10_000_000  # 10 MB

def check_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read(2000).lower()

        if "<?php" in content or "<?=" in content:
            return True
        else:
            return False
    except Exception as e:
        print(f"[ERROR] Could not read file '{filepath}': {e}\n")
        return False

def is_php_file(filepath): 
    size = os.path.getsize(filepath)

    if size == 0:
        return False
    
    if size > max_file_size:
        return False

    return check_file_content(filepath)

    
def processing_file(filepath):
    result = {
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "file_size": os.path.getsize(filepath)
    }

    if not is_php_file(filepath):
        result.update({
            "status": "skipped",
            "prediction": "N/A",
            "reason": "Not a PHP file",
        })
        return result
    
    #ekstraksi
    features = extract_features(filepath)

    if features is None:
        result.update({
            "status": "error",
            "prediction": "N/A",
            "reason": "Feature extraction failed",
        })
        return result

    features_df = pd.DataFrame([features])
    features_df = features_df.reindex(columns=feature_columns, fill_value=0)

    pred = model.predict(features_df)[0]
    proba = model.predict_proba(features_df)[0]
    
    proba_normal = proba[0]
    proba_webshell = proba[1]

    if proba_webshell > proba_normal:
        proba = f"{proba_webshell:.2%}"
    else:
        proba = f"{proba_normal:.2%}"
    
    label = "webshell" if str(pred).lower() == "webshell" or pred == 1 else "normal"

    result.update({
        "status": "processed",
        "prediction": label,
        "confidence": proba,
        "features": features
    })

    return result

def save_result_to_json(result, output_file):
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []
    data.append(result)

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)


def get_status_color(status):
    if status == "processed":
        return Fore.GREEN
    elif status == "skipped":
        return Fore.YELLOW
    elif status == "error":
        return Fore.RED
    else:
        return Fore.GRAY


def detect_file(filepath, output_file=None):
    result = processing_file(filepath)
    color = get_status_color(result["status"])


    if result["status"] == "processed" and "features" in result:
        print(color + "\n" + "=" * 50)
        print(color + "EXTRACTION FEATURES".center(50))
        print(color + "=" * 50)
        for k, v in result["features"].items():
            print(color + f"{k:<35} : {v}")
        print(color + "=" * 50 + Style.RESET_ALL)
        sys.stdout.flush()
    
    print(color + "\n" + "=" * 50)
    print(color + "SUMMARY RESULT".center(50))
    print(color + "=" * 50)
    print(color + f"Status       : {result['status']}")
    print(color + f"File Size    : {os.path.getsize(filepath)} bytes")
    if result["status"] == "processed":
        print(color + f"Prediction   : {result['prediction'].upper()}")
        print(color + f"Confidence   : {result['confidence']}")
    else :
        print(color + f"Reason       : {result['reason']}")
        print(color + f"File Content : {check_file_content(filepath)}")
    print(color + "=" * 50)

    if output_file:
        save_result_to_json(result, output_file)
        print(Fore.GREEN + f"Result Saved to {output_file}")

    print(Style.RESET_ALL)
    sys.stdout.flush()
        
    return result

    