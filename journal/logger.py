import json
import os
from datetime import datetime


class Journal:

    def __init__(self):

        self.file = "journal/history.json"

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:
                json.dump([], f)

    def save(self, analysis):

        record = {

            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "symbol": analysis["symbol"],

            "confidence": analysis["confidence"],

            "grade": analysis["grade"],

            "decision": analysis["decision"],

            "entry": analysis["execution_plan"]["Entry"],

            "stop_loss": analysis["execution_plan"]["Stop Loss"],

            "tp1": analysis["execution_plan"]["TP1"],

            "tp2": analysis["execution_plan"]["TP2"],

            "market_bias": analysis["market_bias"]["Market Bias"],

            "trend": analysis["trend"],

            "bos": analysis["bos"]["BOS"],

            "choch": analysis["choch"]["CHoCH"],

            "liquidity": analysis["liquidity"]["Liquidity"],

            "market_state": analysis["market_state"],

            "confluence": analysis["confluence"],

            "reasoning": analysis["reasoning"],

            "narrative": analysis["narrative"]

        }

        with open(self.file, "r") as f:
            data = json.load(f)

        data.append(record)

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)