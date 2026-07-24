from engine.analyze import run_analysis

WATCHLIST = [
    "GBPUSD",
    "XAUUSD",
    "EURUSD",
    "USDJPY"
]

def dashboard_analysis():

    signals = []

    for symbol in WATCHLIST:

        result = run_analysis(symbol)

        if result:

            print(result["decision"])
            print(type(result["decision"]))

            signals.append({
                "symbol": result["symbol"],
                "decision": result["decision"],
                "confidence": result["confidence"],
                "grade": result["grade"],
                "trend": result["trend"],

                "supply_high": result["supply_demand"]["Supply Zone"]["high"],
                "supply_low": result["supply_demand"]["Supply Zone"]["low"],

                "demand_high": result["supply_demand"]["Demand Zone"]["high"],
                "demand_low": result["supply_demand"]["Demand Zone"]["low"]
            })

    return signals