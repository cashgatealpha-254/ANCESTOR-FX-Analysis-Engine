import MetaTrader5 as mt5


class MarketContext:

    def get(self, symbol):

        tick = mt5.symbol_info_tick(
            symbol
        )

        if tick is None:

            return {
                "status": "NO_DATA",
                "symbol": symbol
            }

        bid = float(
            tick.bid
        )

        ask = float(
            tick.ask
        )

        mid = (
            bid + ask
        ) / 2

        spread = (
            ask - bid
        )

        return {

            "status": "OK",

            "symbol": symbol,

            "bid": bid,

            "ask": ask,

            "mid": mid,

            "spread": spread
        }