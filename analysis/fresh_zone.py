def analyze_fresh_zone(df, supply_demand):

    zone = supply_demand.get("Current Zone", "UNKNOWN")

    # Placeholder logic
    # Later we'll detect retests using candle history.

    if zone in ["Demand", "Supply"]:
        freshness = "Fresh"
    else:
        freshness = "Unknown"

    return {
        "Freshness": freshness
    }