def analyze_supply_demand(df):

    lookback = 20

    recent = df.tail(lookback)

    supply_high = recent["high"].max()
    supply_low = recent["high"].nlargest(3).min()

    demand_low = recent["low"].min()
    demand_high = recent["low"].nsmallest(3).max()

    current_price = recent["close"].iloc[-1]

    if abs(current_price - supply_high) < abs(current_price - demand_low):
        zone = "Supply"
    elif abs(current_price - demand_low) < abs(current_price - supply_high):
        zone = "Demand"
    else:
        zone = "Neutral"

    return {
        "Current Zone": zone,

        "Supply Zone": {
            "high": round(supply_high, 5),
            "low": round(supply_low, 5)
        },

        "Demand Zone": {
            "high": round(demand_high, 5),
            "low": round(demand_low, 5)
        }
    }