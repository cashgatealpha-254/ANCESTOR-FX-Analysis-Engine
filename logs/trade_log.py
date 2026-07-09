from datetime import datetime, timezone


class TradeLogger:

    def __init__(self):
        pass

    def log(self, analysis):

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "analysis": analysis
        }