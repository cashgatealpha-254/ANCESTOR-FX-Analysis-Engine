# engine/summary.py

def build(results):

    report = results.get("report", {})
    verdict = results.get("verdict", {})

    return {
        "symbol": report.get("symbol"),

        "status": verdict.get("status"),

        "grade": report.get("grade"),

        "confidence": report.get("confidence"),

        "bias": results.get("market_bias", {}).get("Market Bias"),

        "trend": results.get("trend", {}).get("Trend"),

        "setup": report.get("setup"),

        "trade_allowed": report.get("trade_allowed")
    }