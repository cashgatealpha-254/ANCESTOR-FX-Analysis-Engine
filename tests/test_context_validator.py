from environment.context_validator import ContextValidator


def main():

    validator = ContextValidator()

    valid_context = {

        "symbol": "GBPUSD",

        "horizon": "SWING",

        "direction": "BEARISH",

        "trend": {},

        "smc": {},

        "liquidity": {},

        "market_profile": {},

        "location": {},

        "relevant_zones": {},

        "confluence": {}
    }

    invalid_context = {

        "symbol": "GBPUSD",

        "horizon": "SCALPING",

        "direction": "INVALID"
    }

    print("=" * 70)
    print("CONTEXT VALIDATOR TEST")
    print("=" * 70)

    result = validator.validate(
        valid_context
    )

    print()
    print("VALID CONTEXT")
    print(f"VALID: {result['valid']}")
    print(f"ERRORS: {result['errors']}")

    result = validator.validate(
        invalid_context
    )

    print()
    print("INVALID CONTEXT")
    print(f"VALID: {result['valid']}")
    print(f"ERRORS: {result['errors']}")


if __name__ == "__main__":
    main()