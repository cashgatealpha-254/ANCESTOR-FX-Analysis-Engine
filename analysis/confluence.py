def analyze_confluence(results):

    score = 0
    aligned = []
    conflicting = []

    bias = results["market_bias"]["Market Bias"]

    if bias == "Bullish":

        checks = [

            ("Trend",
             results["trend"]["Trend"] == "Bullish"),

            ("BOS",
             results["bos"]["BOS"] == "Bullish BOS"),

            ("CHoCH",
             results["choch"]["CHoCH"] == "Bullish"),

            ("Supply & Demand",
             results["supply_demand"]["Current Zone"] == "Demand"),

            ("Liquidity",
             results["liquidity"]["Liquidity"] == "Buy Side"),

            ("Structure",
             results["market_structure"]["Structure"] == "Bullish"),

            ("Structure Memory",
             results["structure_memory"]["Trend"] == "Bullish"),

            ("Protected Levels",
             results["protected_levels"]["Protected Low"] is not None),

            ("Structure Strength",
             results["structure_strength"]["Structure Strength"] == "Strong")

        ]

    else:

        checks = [

            ("Trend",
             results["trend"]["Trend"] == "Bearish"),

            ("BOS",
             results["bos"]["BOS"] == "Bearish BOS"),

            ("CHoCH",
             results["choch"]["CHoCH"] == "Bearish"),

            ("Supply & Demand",
             results["supply_demand"]["Current Zone"] == "Supply"),

            ("Liquidity",
             results["liquidity"]["Liquidity"] == "Sell Side"),

            ("Structure",
             results["market_structure"]["Structure"] == "Bearish"),

            ("Structure Memory",
             results["structure_memory"]["Trend"] == "Bearish"),

            ("Protected Levels",
             results["protected_levels"]["Protected High"] is not None),

            ("Structure Strength",
             results["structure_strength"]["Structure Strength"] == "Strong")

        ]

    for module, passed in checks:
        if passed:
            score += 1
            aligned.append(module)
        else:
            conflicting.append(module)

    max_score = len(checks)

    if score >= 8:
        strength = "High"
    elif score >= 5:
        strength = "Medium"
    else:
        strength = "Low"

    return {
        "Score": score,
        "Max Score": max_score,
        "Strength": strength,
        "Aligned Modules": aligned,
        "Conflicting Modules": conflicting,
        "Summary": f"{score}/{max_score} modules agree with the {bias.lower()} bias."
    }