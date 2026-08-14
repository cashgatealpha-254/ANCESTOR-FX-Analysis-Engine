import MetaTrader5 as mt5


class MarketContext:

    def get(self, symbol):

        symbol = str(symbol).upper()

        # Ensure MT5 is initialized.
        if not mt5.initialize():

            return {
                "status": "NO_DATA",
                "symbol": symbol,
                "reason": "MT5 initialization failed"
            }

        tick = mt5.symbol_info_tick(
            symbol
        )

        if tick is None:

            return {
                "status": "NO_DATA",
                "symbol": symbol,
                "reason": "No data available for the requested symbol"
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