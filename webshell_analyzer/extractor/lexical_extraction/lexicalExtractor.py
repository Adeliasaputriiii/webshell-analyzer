import re

DANGEROUS_FUNCS = ["eval", "system", "exec"]
USER_INPUTS = [r"\$_POST", r"\$_REQUEST", r"\$_FILES"]
INCLUDE_FUNCS = ["require_once"]
SYMBOL_PATTERN = r"[{}\[\]\(\);$]"


def count_regex(pattern, text):
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def extract_lexical_features(code):
    features = {}
    #dangerous functions
    for f in DANGEROUS_FUNCS:
        features[f"lex_func_{f}"] = count_regex(rf"\b{f}\b", code)

    #user input variable
    for var in USER_INPUTS:
        clean_name = var.replace("\\", "").replace("$", "")
        features[f"lex_input_{clean_name}"] = count_regex(var, code)

    #include function
    for inc in INCLUDE_FUNCS:
        features[f"lex_include_{inc}"] = count_regex(rf"\b{inc}\b", code)

    #special symbols
    features["lex_symbol_count"] = count_regex(SYMBOL_PATTERN, code)

    return features
