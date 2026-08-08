import json
import os
from datetime import datetime


class Journal:

    def __init__(self):
        self.file = "journal/history.json"

        os.makedirs(
            os.path.dirname(self.file),
            exist_ok=True
        )

        if not os.path.exists(self.file):
            self._write([])

    def _read(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def save(self, record):
        data = self._read()

        record = {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            **record
        }

        data.append(record)
        self._write(data)

        return record