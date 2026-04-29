import re
import math
import zlib
from collections import Counter


def calculate_entropy(text):
    if not text:
        return 0.0
    
    counter = Counter(text)
    length = len(text)
    return -sum(
        (count / length) * math.log2(count / length)
        for count in counter.values()
    )

def compression_ratio(text):
    if not text:
        return 0.0
    
    encoded = text.encode("utf-8", errors="ignore")

    if len(encoded) == 0:
        return 0.0
    
    compressed = zlib.compress(encoded)
    return len(compressed) / len(encoded)



def extract_statistical_features(php_code):
    if not isinstance(php_code, str):
        php_code = ""

    length = len(php_code)

    features = {
        "stat_entropy": 0,
        "stat_digit_ratio": 0,
        "stat_symbol_ratio": 0,
        "stat_compression_ratio": 0
    }

    if length == 0:
        return features
            
    features["stat_entropy"] = calculate_entropy(php_code)
    features["stat_digit_ratio"] = sum(c.isdigit() for c in php_code) / length
    features["stat_symbol_ratio"] = sum(not c.isalnum() for c in php_code) / length
    features["stat_compression_ratio"] = compression_ratio(php_code)

    return features

