import os
import pickle
import pandas as pd
import json
from joblib import dump, load


base_dir = os.path.dirname(os.path.dirname(__file__))

def load_feature_columns():
    feature_path = os.path.join(base_dir, "model", "features_selected.json")
    with open(feature_path, "r") as f:
        cols = json.load(f)
    return cols

def load_model():
    model_path = os.path.join(base_dir, "model", "rf_webshell_model.joblib")
    return load(model_path)

