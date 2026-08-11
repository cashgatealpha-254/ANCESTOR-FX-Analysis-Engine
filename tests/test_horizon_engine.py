import MetaTrader5 as mt5

from environment.horizon_engine import HorizonEngine


if not mt5.initialize():

    print("MT5 initialization failed")
    print(mt5.last_error())

    raise SystemExit


engine = HorizonEngine()

symbols = [
    "GBPUSD",
    "EURUSD",
    "USDJPY",
    "XAUUSD",
    "DE30"
]


for symbol in symbols:

    print("\n" + "=" * 70)
    print(symbol)

    result = engine.analyze(symbol)

    for horizon, data in result.items():

        print(f"\n--- {horizon} ---")

        if data.get("status") != "OK":

            print(f"Status: {data.get('status')}")
            print(f"Error: {data.get('error', 'N/A')}")
            continue

        print("Status: OK")
        print(f"Bars: {data.get('bars')}")

        # ==========================================
        # DIRECTION
        # ==========================================

        print(
            f"Direction: "
            f"{data.get('direction')}"
        )

        # ==========================================
        # TREND
        # ==========================================

        trend = data.get("trend", {})

        if isinstance(trend, dict):

            print(
                f"Trend: "
                f"{trend.get('trend', 'N/A')}"
            )

        # ==========================================
        # SMC
        # ==========================================

        smc = data.get("smc", {})

        if isinstance(smc, dict):

            print(
                f"Structure Bias: "
                f"{smc.get('structure_bias', 'N/A')}"
            )

            structure = smc.get(
                "structure",
                []
            )

            print(
                f"Latest Structure: "
                f"{structure[-1] if structure else 'None'}"
            )

            breaks = smc.get(
                "structure_breaks",
                []
            )

            print(
                f"Latest Break: "
                f"{breaks[-1] if breaks else 'None'}"
            )

            mss = smc.get(
                "mss",
                {}
            )

            print(
                f"MSS: "
                f"{mss.get('mss', False)}"
            )

            print(
                f"MSS Direction: "
                f"{mss.get('direction', 'N/A')}"
            )

            print(
                f"MSS Type: "
                f"{mss.get('type', 'None')}"
            )

        # ==========================================
        # LIQUIDITY
        # ==========================================

        liquidity = data.get(
            "liquidity",
            {}
        )

        print(
            f"Liquidity: "
            f"{liquidity}"
        )

        # ==========================================
        # RELEVANT ZONES
        # ==========================================

        relevant_zones = data.get(
            "relevant_zones",
            {}
        )

        if isinstance(
            relevant_zones,
            dict
        ):

            print(
                f"Relevant FVGs: "
                f"{len(relevant_zones.get('fvg', []))}"
            )

            print(
                f"Relevant OBs: "
                f"{len(relevant_zones.get('order_blocks', []))}"
            )

        # ==========================================
        # LOCATION
        # ==========================================

        location = data.get(
            "location",
            {}
        )

        print(
            f"Location: "
            f"{location}"
        )

        # ==========================================
        # CONFLUENCE
        # ==========================================

        confluence = data.get(
            "confluence",
            {}
        )

        print(
            f"Confluence: "
            f"{confluence}"
        )


mt5.shutdown()