import json
import os
from collections import Counter


class MarketMemory:

    def __init__(self):

        self.file = "brain/memory.json"

        os.makedirs(os.path.dirname(self.file), exist_ok=True)

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:
                json.dump([], f)

    def load(self):

        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, data):

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def record(self, results):

        data = self.load()

        record = {

            "symbol": results["symbol"],

            "bias": results["market_bias"]["Market Bias"],

            "trend": results["trend"]["Trend"],

            "bos": results["bos"]["BOS"],

            "choch": results["choch"]["CHoCH"],

            "zone": results["supply_demand"]["Current Zone"],

            "liquidity": results["liquidity"]["Liquidity"],

            "strength": results["structure_strength"]["Structure Strength"],

            "confidence": results["confidence"],

            "decision": results["decision"],

            "grade": results["grade"],

            "trade_allowed": results.get("trade_allowed", False),

            "outcome": results.get("outcome", "Pending")

        }

        data.append(record)

        self.save(data)

    def find_similar(self, results):

        data = self.load()

        similar = []

        for record in data:

            if (

                record["bias"] == results["market_bias"]["Market Bias"]

                and record["trend"] == results["trend"]["Trend"]

                and record["bos"] == results["bos"]["BOS"]

                and record["zone"] == results["supply_demand"]["Current Zone"]

                and record["liquidity"] == results["liquidity"]["Liquidity"]

            ):

                similar.append(record)

        return similar

    def historical_probability(self, results):

        trades = self.find_similar(results)

        if len(trades) == 0:

            return {

                "Probability": 0,

                "Wins": 0,

                "Losses": 0,

                "Sample Size": 0

            }

        wins = len(

            [

                x for x in trades

                if x["outcome"] in ["TP1", "TP2", "Win"]

            ]

        )

        losses = len(

            [

                x for x in trades

                if x["outcome"] in ["SL", "Loss"]

            ]

        )

        probability = round((wins / len(trades)) * 100, 2)

        return {

            "Probability": probability,

            "Wins": wins,

            "Losses": losses,

            "Sample Size": len(trades)

        }

    def best_conditions(self):

        data = self.load()

        wins = [

            x for x in data

            if x["outcome"] in ["TP1", "TP2", "Win"]

        ]

        return Counter(

            (

                x["bias"],

                x["zone"],

                x["liquidity"]

            )

            for x in wins

        ).most_common(5)

    def worst_conditions(self):

        data = self.load()

        losses = [

            x for x in data

            if x["outcome"] in ["SL", "Loss"]

        ]

        return Counter(

            (

                x["bias"],

                x["zone"],

                x["liquidity"]

            )

            for x in losses

        ).most_common(5)