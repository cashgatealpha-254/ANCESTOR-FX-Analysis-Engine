from environment.deep_context_store import DeepContextStore


def print_section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_horizon(horizon, context):

    print()
    print(f"[{horizon}]")

    if not isinstance(context, dict):
        print("No context available.")
        return

    print(f"Direction: {context.get('direction')}")
    print(f"Timeframe: {context.get('timeframe')}")
    print(f"Bars: {context.get('bars')}")

    # ---------------------------------------------
    # TREND
    # ---------------------------------------------

    trend = context.get("trend")

    print()
    print("TREND")
    print("-" * 40)

    if isinstance(trend, dict):

        for key, value in trend.items():
            print(f"{key}: {value}")

    else:
        print(trend)

    # ---------------------------------------------
    # SMC
    # ---------------------------------------------

    smc = context.get("smc")

    print()
    print("SMC")
    print("-" * 40)

    if isinstance(smc, dict):

        for key, value in smc.items():
            print(f"{key}: {value}")

    else:
        print(smc)

    # ---------------------------------------------
    # LIQUIDITY
    # ---------------------------------------------

    liquidity = context.get("liquidity")

    print()
    print("LIQUIDITY")
    print("-" * 40)

    if isinstance(liquidity, dict):

        for key, value in liquidity.items():
            print(f"{key}: {value}")

    else:
        print(liquidity)

    # ---------------------------------------------
    # MARKET PROFILE
    # ---------------------------------------------

    profile = context.get("market_profile")

    print()
    print("MARKET PROFILE")
    print("-" * 40)

    if isinstance(profile, dict):

        for key, value in profile.items():
            print(f"{key}: {value}")

    else:
        print(profile)

    # ---------------------------------------------
    # LOCATION
    # ---------------------------------------------

    location = context.get("location")

    print()
    print("LOCATION")
    print("-" * 40)

    if isinstance(location, dict):

        for key, value in location.items():
            print(f"{key}: {value}")

    else:
        print(location)

    # ---------------------------------------------
    # RELEVANT ZONES
    # ---------------------------------------------

    zones = context.get("relevant_zones")

    print()
    print("RELEVANT ZONES")
    print("-" * 40)

    if isinstance(zones, dict):

        for key, value in zones.items():
            print(f"{key}: {value}")

    else:
        print(zones)

    # ---------------------------------------------
    # CONFLUENCE
    # ---------------------------------------------

    confluence = context.get("confluence")

    print()
    print("CONFLUENCE")
    print("-" * 40)

    if isinstance(confluence, dict):

        for key, value in confluence.items():
            print(f"{key}: {value}")

    else:
        print(confluence)


def main():

    print("=" * 70)
    print("ANCESTOR FX DEEP CONTEXT INSPECTION")
    print("=" * 70)

    store = DeepContextStore()

    symbol = "GBPUSD"

    for horizon in [
        "SWING",
        "INTRADAY",
        "SCALPING"
    ]:

        snapshot = store.load(
            symbol,
            horizon
        )

        print_section(
            f"{symbol} {horizon}"
        )

        if snapshot is None:

            print(
                f"No stored context found "
                f"for {symbol} {horizon}"
            )

            continue

        context = snapshot.get(
            "context",
            {}
        )

        print(
            f"Context version: "
            f"{snapshot.get('context_version')}"
        )

        print(
            f"Analysis time: "
            f"{snapshot.get('analysis_time')}"
        )

        print_horizon(
            horizon,
            context
        )

    print()
    print("=" * 70)
    print("INSPECTION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()