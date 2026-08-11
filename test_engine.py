from engine.analyze import run_analysis


def main():

    symbol = "GBPUSD"

    print()
    print("=" * 70)
    print("MARKET ANALYSIS ENGINE TEST")
    print("=" * 70)

    print()
    print(f"Testing: {symbol}")
    print()

    try:

        result = run_analysis(symbol)

        if not isinstance(result, dict):

            print("RESULT: FAIL")
            print("Reason: Engine did not return a dictionary.")
            return

        print("RESULT: ENGINE RETURNED DATA")
        print()

        print(
            f"Symbol: "
            f"{result.get('symbol', symbol)}"
        )

        print(
            f"Decision: "
            f"{result.get('decision', 'N/A')}"
        )

        print(
            f"Confidence: "
            f"{result.get('confidence', 'N/A')}"
        )

        print(
            f"Grade: "
            f"{result.get('grade', 'N/A')}"
        )

        print()

        # ------------------------------------------------
        # CORE OUTPUT CHECKS
        # ------------------------------------------------

        required_fields = [
            "decision",
            "confidence",
            "grade",
        ]

        print("CORE OUTPUT CHECKS")
        print("-" * 40)

        passed = True

        for field in required_fields:

            exists = field in result

            print(
                f"{field}: "
                f"{'PASS' if exists else 'FAIL'}"
            )

            if not exists:
                passed = False

        # ------------------------------------------------
        # OPTIONAL ENGINE OUTPUTS
        # ------------------------------------------------

        optional_fields = [
            "trend",
            "market_bias",
            "market_state",
            "market_structure",
            "bos",
            "choch",
            "liquidity",
            "supply_demand",
            "confidence_breakdown",
            "execution_plan",
            "risk",
            "narrative",
            "reasoning",
        ]

        print()
        print("ENGINE OUTPUT CHECK")
        print("-" * 40)

        for field in optional_fields:

            status = (
                "AVAILABLE"
                if field in result
                else "MISSING"
            )

            print(
                f"{field}: {status}"
            )

        # ------------------------------------------------
        # FINAL RESULT
        # ------------------------------------------------

        print()
        print("=" * 70)

        if passed:

            print("RESULT: PASS")

        else:

            print("RESULT: FAIL")

        print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)
        print("RESULT: ENGINE ERROR")
        print("=" * 70)

        print()
        print(
            f"{type(error).__name__}: "
            f"{error}"
        )


if __name__ == "__main__":

    main()