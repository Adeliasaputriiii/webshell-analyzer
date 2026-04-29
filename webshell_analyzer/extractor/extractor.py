import os
import subprocess
import json
from webshell_analyzer.extractor.statistical_extraction.statisticalExtractor import extract_statistical_features
from webshell_analyzer.extractor.lexical_extraction.lexicalExtractor import extract_lexical_features
from webshell_analyzer.model.model_loader import load_feature_columns

feature_columns = load_feature_columns()

base_dir = os.path.dirname(os.path.dirname(__file__))

def extract_ast(filepath):
    # Gunakan os.path.abspath untuk memastikan path absolut benar
    php_ast_path = os.path.abspath(os.path.join(base_dir, "extractor", "ast_extraction", "src", "astExtractor.php"))
    target_file = os.path.abspath(filepath)

    try:
        # Gunakan list argumen, subprocess akan menangani spasi secara otomatis
        # Namun pastikan executable 'php' terdaftar di PATH Windows Anda
        result = subprocess.run(["php", php_ast_path, target_file], capture_output=True, text=True)

        if result.returncode != 0:
            # Jika stderr kosong, kita cek stdout (siapa tahu PHP error tapi keluar di stdout)
            print(f"\n[DEBUG] PHP Exit Code: {result.returncode}")
            print(f"[DEBUG] PHP STDERR: {result.stderr}")
            print(f"[DEBUG] PHP STDOUT: {result.stdout}")
            return None
        
        return json.loads(result.stdout)
    except Exception as e:
        print(f"[DEBUG] Python Exception: {e}")
        return None


def align_features(features_dict):
    return [features_dict.get(col, 0) for col in feature_columns]


def extract_features(filepath):
    features = {}

    # =====================
    # AST (OPTIONAL)
    # =====================
    ast_features = extract_ast(filepath)
    if ast_features is None:
        print("[WARN] AST extraction failed")
    else:
        features.update(ast_features)

    # =====================
    # READ FILE
    # =====================
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read().strip()
    except Exception as e:
        print("[ERROR] Failed to read file:", e)
        return None

    # =====================
    # LEXICAL (WAJIB)
    # =====================
    try:
        lexical_features = extract_lexical_features(code)
        features.update(lexical_features)
    except Exception as e:
        print("[ERROR][LEXICAL]", e)

    # =====================
    # STATISTICAL (WAJIB)
    # =====================
    try:
        statistical_features = extract_statistical_features(code)
        features.update(statistical_features)
    except Exception as e:
        print("[ERROR][STATISTICAL]", e)

    # =====================
    # FINAL CHECK
    # =====================
    if not features:
        print("[ERROR] All feature extraction failed")
        return None

    return features