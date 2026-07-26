def show(results):

    bias = results["market_bias"]["Market Bias"]
    trend = results["trend"]["Trend"]
    state = results["market_state"]["Market State"]
    structure = results["market_structure"]["Structure"]

    print("\nMARKET SNAPSHOT")
    print("-" * 50)

    print(f"Bias      : {bias}")
    print(f"Trend     : {trend}")
    print(f"State     : {state}")
    print(f"Structure : {structure}")