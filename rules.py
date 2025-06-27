# rules.py

import json

RULES_FILE = "rules.json"

def save_rules(rules, weights):
    data = {
        "rules": rules,
        "weights": weights
    }
    with open(RULES_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return True

def load_rules():
    try:
        with open(RULES_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"rules": [], "weights": {}}
