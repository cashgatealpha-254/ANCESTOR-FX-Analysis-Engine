import json
import os

MEMORY_FILE = "memory/history.json"


def load_history():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):

    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def get_recent_history(n=10):
    history = load_history()
    return history[-n:] if len(history) >= n else history        

def get_symbol_history(symbol, n=10):
    history = load_history()
    symbol_history = [entry for entry in history if entry["symbol"] == symbol]
    return symbol_history[-n:] if len(symbol_history) >= n else symbol_history

def average_confidence(symbol, n=10):
    symbol_history = get_symbol_history(symbol, n)
    if not symbol_history:
        return None
    total_confidence = sum(entry["confidence"] for entry in symbol_history)
    return total_confidence / len(symbol_history)

        