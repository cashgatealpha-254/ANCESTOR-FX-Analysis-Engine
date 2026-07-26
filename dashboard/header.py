from datetime import datetime


def show(symbol, health):

    print("=" * 50)
    print("        ANCESTOR FX ENGINE")
    print("=" * 50)

    print(f"Symbol : {symbol}")

    print(
        f"Time   : {datetime.now().strftime('%H:%M:%S')}"
    )

    if health["healthy"]:
        print("Status : 🟢 ENGINE ONLINE")

    else:
        print("Status : 🔴 ENGINE OFFLINE")

    print("=" * 50)