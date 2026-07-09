class ChecklistEngine:

    def __init__(self):
        pass

    def evaluate(self, analysis):

        checklist = {

            "Trend": analysis["trend"] in ["Bullish", "Bearish"],

            "Confidence": analysis["confidence"] >= 80,

            "Session": analysis["session"] != "ASIAN",

            "Bias": analysis["market_bias"] in ["BUY", "SELL"],

            "BOS": analysis["bos"]["BOS"] != "No BOS"

        }

        score = sum(checklist.values())

        return {
            "score": score,
            "maximum": len(checklist),
            "items": checklist
        }