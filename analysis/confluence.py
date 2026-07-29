def analyze_confluence(results):

    score = 0

    aligned = []
    conflicting = []

    bias = results["market_bias"]["Market Bias"]

    weights = {

        "Trend": 2,
        "BOS": 2,
        "CHoCH": 2,
        "Supply & Demand": 2,
        "Liquidity": 1,
        "Structure": 2,
        "Structure Memory": 2,
        "Protected Levels": 1,
        "Structure Strength": 2

    }

    if bias == "Bullish":

        checks = [

            ("Trend",
             results["trend"]["Trend"] == "Bullish"),

            ("BOS",
             results["bos"]["BOS"] == "Bullish BOS"),

            ("CHoCH",
             results["choch"]["CHoCH"] == "Bullish CHoCH"),

            ("Supply & Demand",
             results["supply_demand"]["Current Zone"] == "Demand"),

            ("Liquidity",
             results["liquidity"]["Liquidity"] == "Sell-side Liquidity Swept"),

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
             results["choch"]["CHoCH"] == "Bearish CHoCH"),

            ("Supply & Demand",
             results["supply_demand"]["Current Zone"] == "Supply"),

            ("Liquidity",
             results["liquidity"]["Liquidity"] == "Buy-side Liquidity Swept"),

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

            score += weights[module]

            aligned.append({

                "Module": module,
                "Weight": weights[module]

            })

        else:

            conflicting.append({

                "Module": module,
                "Weight": weights[module]

            })

    max_score = sum(weights.values())

    percentage = round((score / max_score) * 100, 1)

    if percentage >= 80:
        strength = "High"

    elif percentage >= 60:
        strength = "Medium"

    else:
        strength = "Low"

    return {

        "Score": score,

        "Max Score": max_score,

        "Percentage": percentage,

        "Strength": strength,

        "Aligned Modules": aligned,

        "Conflicting Modules": conflicting,

        "Summary":
        f"{score}/{max_score} ({percentage}%) confluence with {bias.lower()} bias."

    }