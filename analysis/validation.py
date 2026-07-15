def validate_analysis(results):

    errors = []

    required = [
        "trend",
        "market_bias",
        "market_structure",
        "supply_demand",
        "liquidity",
        "bos",
        "choch",
        "decision",
        "setup",
        "execution",
        "risk"
    ]

    for key in required:
        if results.get(key) is None:
            errors.append(f"{key} missing")

    return {
        "Valid": len(errors) == 0,
        "Errors": errors
    }