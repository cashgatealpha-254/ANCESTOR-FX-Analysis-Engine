def analyze_supply_demand(df, swings):

    swing_highs = swings["swing_highs"]
    swing_lows = swings["swing_lows"]

    if not swing_highs or not swing_lows:
        return None
    
    lookback = 20
    recent = df.tail(lookback)
    
    last_supply = swing_highs[-1]
    last_demand = swing_lows[-1]

    supply_high = last_supply["price"]
    supply_low = supply_high - 0.0010   # temporary zone width

    demand_low = last_demand["price"]
    demand_high = demand_low + 0.0010   # temporary zone width

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