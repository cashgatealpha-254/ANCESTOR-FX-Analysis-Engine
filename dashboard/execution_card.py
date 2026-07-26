def show(report):

    print("\nEXECUTION")
    print("-" * 50)

    print(f"Entry      : {report['entry']}")
    print(f"Stop Loss  : {report['stop_loss']}")
    print(f"Take Profit: {report['take_profit']}")
    print(f"RR         : {report['risk_reward']}")