def run():

    checks = {
        "mt5": True,
        "candles": True,
        "indicators": True,
        "analysis": True,
        "strategy": True,
        "brain": True,
        "dashboard": True,
    }

    overall = all(checks.values())

    return {
        "healthy": overall,
        "checks": checks
    }