import MetaTrader5 as mt5

from execution.mt5_markup_publisher import MT5MarkupPublisher


if not mt5.initialize():
    print("MT5 initialization failed")
    print("Error:", mt5.last_error())
    raise SystemExit


publisher = MT5MarkupPublisher()

result = publisher.publish(
    symbol="GBPUSD",
    horizon="INTRADAY",

    zones=[
        {
            "type": "FVG",
            "direction": "BULLISH",
            "low": 1.1500,
            "high": 1.1520
        },
        {
            "type": "ORDER_BLOCK",
            "direction": "BULLISH",
            "low": 1.1470,
            "high": 1.1490
        }
    ],

    liquidity=[
        {
            "type": "BUY_SIDE",
            "price": 1.1580
        }
    ],

    trade_setup={
        "entry": 1.1510,
        "stop_loss": 1.1460,
        "take_profit": 1.1610
    }
)

print(result)

mt5.shutdown()