# environment/deep_context_engine.py

from datetime import datetime

from environment.deep_context_config import (
    get_symbols,
    get_horizon_timeframes,
)

from environment.deep_context_data import (
    fetch_timeframe_context,
)


class DeepContextEngine:

    def __init__(self):

        self.context = {}

    # ========================================================
    # BUILD CONTEXT FOR ONE SYMBOL
    # ========================================================

    def build_symbol_context(self, symbol):

        symbol = symbol.upper()

        symbol_context = {
            "symbol": symbol,
            "created_at": datetime.now().isoformat(),
            "timeframes": {},
            "horizons": {},
        }

        # ----------------------------------------------------
        # FETCH EACH TIMEFRAME ONLY ONCE
        # ----------------------------------------------------

        all_timeframes = set()

        for horizon in [
            "SWING",
            "INTRADAY",
            "SCALPING",
        ]:

            timeframes = get_horizon_timeframes(
                horizon
            )

            all_timeframes.update(
                timeframes
            )

        for timeframe_name in all_timeframes:

            try:

                candles = fetch_timeframe_context(
                    symbol,
                    timeframe_name
                )

                symbol_context[
                    "timeframes"
                ][timeframe_name] = {

                    "status": "READY",

                    "candles": candles,

                    "count": len(candles),

                    "start": (
                        candles.index.min()
                        .isoformat()
                    ),

                    "end": (
                        candles.index.max()
                        .isoformat()
                    ),
                }

            except Exception as e:

                symbol_context[
                    "timeframes"
                ][timeframe_name] = {

                    "status": "ERROR",

                    "candles": None,

                    "count": 0,

                    "error": str(e),
                }

        # ----------------------------------------------------
        # BUILD HORIZONS FROM FETCHED DATA
        # ----------------------------------------------------

        for horizon in [
            "SWING",
            "INTRADAY",
            "SCALPING",
        ]:

            horizon_context = {}

            for timeframe_name in (
                get_horizon_timeframes(
                    horizon
                )
            ):

                timeframe_data = (
                    symbol_context[
                        "timeframes"
                    ].get(
                        timeframe_name
                    )
                )

                horizon_context[
                    timeframe_name
                ] = timeframe_data

            symbol_context[
                "horizons"
            ][horizon] = horizon_context

        self.context[symbol] = (
            symbol_context
        )

        return symbol_context

    # ========================================================
    # BUILD ALL SYMBOLS
    # ========================================================

    def build_all(self):

        results = {}

        for symbol in get_symbols():

            try:

                results[symbol] = (
                    self.build_symbol_context(
                        symbol
                    )
                )

            except Exception as e:

                results[symbol] = {

                    "symbol": symbol,

                    "status": "ERROR",

                    "error": str(e),
                }

        return results

    # ========================================================
    # GET STORED CONTEXT
    # ========================================================

    def get(self, symbol):

        return self.context.get(
            symbol.upper()
        )

    # ========================================================
    # GET ONE TIMEFRAME
    # ========================================================

    def get_timeframe(
        self,
        symbol,
        timeframe
    ):

        symbol_context = self.get(
            symbol
        )

        if not symbol_context:
            return None

        return symbol_context[
            "timeframes"
        ].get(
            timeframe
        )

    # ========================================================
    # STATUS
    # ========================================================

    def status(self):

        output = {}

        for symbol, context in (
            self.context.items()
        ):

            output[symbol] = {}

            for timeframe, data in (
                context[
                    "timeframes"
                ].items()
            ):

                output[symbol][
                    timeframe
                ] = {

                    "status":
                        data.get(
                            "status"
                        ),

                    "count":
                        data.get(
                            "count",
                            0
                        ),
                }

        return output