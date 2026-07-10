import json
import os
from datetime import datetime


def save_analysis(symbol, data):
    folder = f"logs/{symbol.upper()}"

    os.makedirs(folder, exist_ok=True)

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.json")

    path = os.path.join(folder, filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    return path