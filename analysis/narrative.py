def build_narrative(results):

    lines = []

    trend = results["trend"]["Trend"]
    bias = results["market_bias"]
    structure = results["market_structure"]["Structure"]
    zone = results["supply_demand"]["Current Zone"]
    liquidity = results["liquidity"]["Liquidity"]

    lines.append(f"Trend is {trend}.")
    lines.append(f"Market bias remains {bias}.")
    lines.append(f"Current structure is {structure}.")
    lines.append(f"Price is trading near {zone}.")
    lines.append(f"Liquidity status: {liquidity}.")

    return " ".join(lines)