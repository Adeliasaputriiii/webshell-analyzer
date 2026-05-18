import os
import sys
import json
from colorama import Fore, Style
import pandas as pd
from sklearn.inspection import permutation_importance
from webshell_analyzer.extractor.extractor import extract_features
from webshell_analyzer.model.model_loader import load_feature_columns, load_model

feature_columns = load_feature_columns()
model = load_model()

max_file_size = 10_000_000  # 10 MB

def check_file_content(filepath):
    try:
        #Read only the first 2000 bytes to check for PHP tags
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read(2000).lower()

        #check if the file contains PHP opening tags
        if "<?php" in content or "<?=" in content:
            return True
        else:
            return False
    except Exception as e:
        print(f"[ERROR] Could not read file '{filepath}': {e}")
        return False

def validate_file(filepath):
    size = os.path.getsize(filepath)

    #check whether the file is empty 
    if size == 0:
        return False, "Empty File, No Content to Analyze"
    
    #validate maximum allowed file size
    if size > max_file_size:
        return False, "File too Large"

    #check whether the file contains PHP code or not, if not skip the file
    if not check_file_content(filepath):
        return False, "No PHP Code Detected"
    
    return True, None


def processing_file(filepath):
    is_valid, reason = validate_file(filepath)

    result = {
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "file_size": os.path.getsize(filepath)
    }

    #if the file is not valid, return the result with status "invalid" and reason for skipping the file
    if not is_valid:
        result.update({
            "status": "invalid",
            "prediction": "N/A",
            "reason": reason,
        })
        return result
    
    #feature extraction
    features = extract_features(filepath)

    #return the result with status "error", if feature extraction fails
    if features is None:
        result.update({
            "status": "error",
            "prediction": "N/A",
            "reason": "Feature extraction failed",
        })
        return result

    features_df = pd.DataFrame([features])
    features_df = features_df.reindex(columns=feature_columns, fill_value=0)

    #model prediction
    pred = model.predict(features_df)[0]
    proba = model.predict_proba(features_df)[0]
    
    proba_normal = proba[0]
    proba_webshell = proba[1]

    #determine the confidence score based on the predicted class with the highest probability
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

#saving the output detection to json file
def save_result_to_json(result, output_file):
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            try:
                data = json.load(f)

                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
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
        return Fore.CYAN
    
def show_save_message(output_file):
    print(Fore.GREEN + "\n" + "-" * 50)
    print(Fore.GREEN + f"OUTPUT FILE SAVED".center(50))
    print(Fore.GREEN + "-" * 50)
    print(Fore.GREEN + f"Location:  {output_file}")
    print(Fore.GREEN + "-" * 50)
    print(Style.RESET_ALL)


def detect_file(filepath, output_file=None):
    result = processing_file(filepath)
    color = get_status_color(result["status"])


    if result["status"] == "processed" and "features" in result:
        print(color + "\n" + "=" * 50)
        print(color + "EXTRACTION FEATURES".center(50))
        print(color + "=" * 50)
        for k, v in result["features"].items():
            nilai = f"{v:.4f}" if isinstance(v, float) else str(v)
            print(color + f"{k:<35} : {nilai}")
        print(color + "=" * 50 + Style.RESET_ALL)
    
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
    print(color + "=" * 50)

    if output_file:
        save_result_to_json(result, output_file)
        show_save_message(output_file)
    return result

    