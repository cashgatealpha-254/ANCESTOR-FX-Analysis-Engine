import json


class JournalReader:

    def __init__(self):
        self.file = "journal/history.json"

    def read(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def latest(self, count=10):
        return self.read()[-count:]