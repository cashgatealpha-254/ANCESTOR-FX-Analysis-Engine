from execution.execution_registry import ExecutionRegistry


def main():

    registry = ExecutionRegistry(
        "execution/test_registry.json"
    )

    setup = {

        "symbol": "EURUSD",

        "horizon": "INTRADAY",

        "direction": "BULLISH",

        "entry": 1.1000,

        "stop_loss": 1.0980,

        "take_profit": 1.1040
    }

    trade_id = (
        registry.build_trade_id(
            setup
        )
    )

    print(
        "Trade ID:",
        trade_id
    )

    first = registry.register(
        trade_id,
        "SUBMITTED",
        setup=setup
    )

    print(
        "First:",
        first
    )

    second = registry.register(
        trade_id,
        "SUBMITTED",
        setup=setup
    )

    print(
        "Second:",
        second
    )

    print(
        "Exists:",
        registry.exists(
            trade_id
        )
    )

    print(
        "Record:",
        registry.get(
            trade_id
        )
    )


if __name__ == "__main__":
    main()