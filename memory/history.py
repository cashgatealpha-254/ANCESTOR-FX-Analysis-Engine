import json
import os
from datetime import datetime

MEMORY_FILE = "memory/history.json"


def load_history():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def append_analysis(data):
    history = load_history()

    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **data
    })

    save_history(history)


def get_symbol_history(symbol):
    history = load_history()

    return [
        trade
        for trade in history
        if trade["symbol"] == symbol.upper()
    ]

def get_recent_history(n=10):
    history = load_history()
    return history[-n:]

def average_confidence(symbol):
    history = get_symbol_history(symbol)
    if not history:
        return None

    total_confidence = sum(item["confidence"] for item in history)
    return round(total_confidence / len(history), 2)