class ExecutionPlanner:

    def __init__(self):
        pass

    def build(self, analysis):

        decision = analysis["decision"]
        confidence = analysis["confidence"]
        setup = analysis["setup"]

        # --------------------------
        # No Trade
        # --------------------------
        if decision == "NO TRADE":
            return {
                "Status": "WAIT"
            }

        # --------------------------
        # Lot Size
        # --------------------------
        if confidence >= 95:
            lot = 0.03

        elif confidence >= 90:
            lot = 0.02

        else:
            lot = 0.01

        # --------------------------
        # Positions
        # --------------------------
        positions = 2

        # --------------------------
        # Build Plan
        # --------------------------
        return {

            "Status": "READY",

            "Direction": decision,

            "Entry": setup["entry"],

            "Stop Loss": setup["stop_loss"],

            "TP1": 100,

            "TP2": 200,

            "Positions": positions,

            "Lot Size": lot,

            "Management": {

                "TP1": "Close Position 1",

                "TP2": "Hold Position 2",

                "After TP1": "Move SL to Break Even"

            }

        }