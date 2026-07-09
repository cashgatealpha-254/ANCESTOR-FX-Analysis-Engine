def analyze_supply_demand(df):

    highest = df["high"].max()
    lowest = df["low"].min()

    current_price = df["close"].iloc[-1]

    supply = highest
    demand = lowest

    if abs(current_price - supply) < abs(current_price - demand):
        zone = "Supply"

    elif abs(current_price - demand) < abs(current_price - supply):
        zone = "Demand"

    else:
        zone = "Neutral"

    return {
        "Current Zone": zone,
        "Supply": round(supply, 5),
        "Demand": round(demand, 5)
    }