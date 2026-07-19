import os
import subprocess
import json
from webshell_analyzer.extractor.statistical_extraction.statisticalExtractor import extract_statistical_features
from webshell_analyzer.extractor.lexical_extraction.lexicalExtractor import extract_lexical_features
from webshell_analyzer.model.model_loader import load_feature_columns

feature_columns = load_feature_columns()

base_dir = os.path.dirname(os.path.dirname(__file__))

def extract_ast(filepath):
    #call the AST extractor script
    php_ast_path = os.path.abspath(os.path.join(base_dir, "extractor", "ast_extraction", "src", "astExtractor.php"))
    target_file = os.path.abspath(filepath)

    try:
        result = subprocess.run(["php", php_ast_path, target_file], capture_output=True, text=True)

        #Handle errors if the PHP script execution fails
        if result.returncode != 0:
            return None
        
        try:
            return json.loads(result.stdout)
        
        #error handling for invalid JSON output from the PHP script
        except json.JSONDecodeError:
            print(f"[WARNING] invalid ast output")

    except Exception:
        return None


def align_features(features_dict):
    return [features_dict.get(col, 0) for col in feature_columns]


def extract_features(filepath):
    features = {}

    #Extract AST features
    ast_features = extract_ast(filepath)
    if ast_features is not None:
        features.update(ast_features)

   
    try:
        #read file content for lexical and statistical extraction
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read().strip()
    except Exception:
        print("[ERROR] Failed to read file")
        return None

    try:
        #extract lexical features
        lexical_features = extract_lexical_features(code)
        features.update(lexical_features)
    except Exception:
        print("[WARNING] Lexical feature extraction failed")

    try:
        #extract statistical features
        statistical_features = extract_statistical_features(code)
        features.update(statistical_features)
    except Exception:
        print("[WARNING] statistical feature extraction failed")

    if not features:
        return None

    return features