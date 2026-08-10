import MetaTrader5 as mt5

from execution.mt5_markup_publisher import MT5MarkupPublisher


def main():

    if not mt5.initialize():

        print("MT5 initialization failed")
        print(mt5.last_error())
        return

    publisher = MT5MarkupPublisher()

    result = publisher.publish(
        symbol="GBPUSD",
        horizon="M15",
        zones=[
            {
                "type": "demand",
                "low": 1.2700,
                "high": 1.2720
            }
        ],
        liquidity=[
            {
                "type": "sell_side",
                "price": 1.2680
            }
        ],
        structure=[
            {
                "type": "BOS",
                "direction": "bullish",
                "price": 1.2740
            }
        ],
        trade_setup={
            "direction": "BUY",
            "entry": 1.2720,
            "stop_loss": 1.2680,
            "take_profit": 1.2800
        }
    )

    print(result)

    clear_result = publisher.clear()

    print(clear_result)

    mt5.shutdown()


if __name__ == "__main__":
    main()