from pathlib import Path
from environment.deep_context_store import DeepContextStore


def main():

    print("=" * 70)
    print("DEEP CONTEXT STORE TEST")
    print("=" * 70)

    test_dir = Path(
        "data/test_deep_context"
    )

    store = DeepContextStore(
        base_dir=test_dir
    )

    context = {

        "symbol": "GBPUSD",

        "horizon": "SWING",

        "direction": "BEARISH",

        "trend": {
            "trend": "BEARISH"
        },

        "smc": {
            "structure": []
        },

        "liquidity": {
            "status": "TEST"
        },

        "market_profile": {
            "poc": 1.3500
        },

        "location": {
            "status": "TEST"
        },

        "relevant_zones": {
            "fvg": [],
            "order_blocks": []
        },

        "confluence": {
            "score": 70
        }
    }

    # ==================================================
    # SAVE
    # ==================================================

    print()
    print("SAVING CONTEXT...")

    saved = store.save(
        symbol="GBPUSD",
        horizon="SWING",
        context=context
    )

    print(
        f"STATUS: "
        f"{saved.get('status', 'OK')}"
    )

    print(
        f"VERSION: "
        f"{saved.get('context_version')}"
    )

    # ==================================================
    # CHECK EXISTS
    # ==================================================

    print()
    print("CHECKING STORAGE...")

    exists = store.exists(
        "GBPUSD",
        "SWING"
    )

    print(
        f"EXISTS: {exists}"
    )

    # ==================================================
    # LOAD
    # ==================================================

    print()
    print("LOADING CONTEXT...")

    loaded = store.load(
        "GBPUSD",
        "SWING"
    )

    if loaded is None:

        print(
            "LOAD FAILED"
        )

        return

    print(
        f"SYMBOL: "
        f"{loaded.get('symbol')}"
    )

    print(
        f"HORIZON: "
        f"{loaded.get('horizon')}"
    )

    print(
        f"VERSION: "
        f"{loaded.get('context_version')}"
    )

    # ==================================================
    # VERIFY
    # ==================================================

    stored_context = loaded.get(
        "context",
        {}
    )

    print()
    print("VERIFYING...")

    checks = {

        "symbol":
            stored_context.get(
                "symbol"
            ) == "GBPUSD",

        "horizon":
            stored_context.get(
                "horizon"
            ) == "SWING",

        "direction":
            stored_context.get(
                "direction"
            ) == "BEARISH",

        "trend":
            isinstance(
                stored_context.get(
                    "trend"
                ),
                dict
            ),

        "market_profile":
            isinstance(
                stored_context.get(
                    "market_profile"
                ),
                dict
            ),

        "relevant_zones":
            isinstance(
                stored_context.get(
                    "relevant_zones"
                ),
                dict
            )
    }

    for name, passed in checks.items():

        print(
            f"{name}: "
            f"{'PASS' if passed else 'FAIL'}"
        )

    # ==================================================
    # FINAL RESULT
    # ==================================================

    if all(checks.values()):

        print()
        print(
            "RESULT: PASS"
        )

    else:

        print()
        print(
            "RESULT: FAIL"
        )


if __name__ == "__main__":

    main()