# environment/deep_context_engine.py

from datetime import datetime

from environment.candle_cache import CandleCache
from environment.horizon_engine import HorizonEngine
from environment.deep_context_store import DeepContextStore
from environment.deep_context_config import get_symbols


class DeepContextEngine:

    def __init__(self):

        self.cache = CandleCache()

        self.horizon_engine = HorizonEngine()

        self.store = DeepContextStore()

        self.context = {}

    # ==================================================
    # BUILD ONE SYMBOL
    # ==================================================

    def build_symbol_context(
        self,
        symbol
    ):

        symbol = symbol.upper()

        print()
        print("=" * 70)
        print(
            f"BUILDING DEEP CONTEXT: {symbol}"
        )
        print("=" * 70)

        # --------------------------------------------------
        # GET CACHED MARKET DATA
        # --------------------------------------------------

        candles = (
            self.cache.build_symbol_context(
                symbol
            )
        )

        if not candles:

            raise ValueError(
                f"No candle context available for {symbol}"
            )

        # --------------------------------------------------
        # ANALYZE HORIZONS
        # --------------------------------------------------

        print()
        print(
            "Running horizon intelligence..."
        )

        horizons = (
            self.horizon_engine.analyze_context(
                symbol,
                candles
            )
        )

        # --------------------------------------------------
        # BUILD FINAL CONTEXT
        # --------------------------------------------------

        symbol_context = {

            "schema_version": "2.0",

            "symbol": symbol,

            "created_at":
                datetime.now().isoformat(),

            "timeframes": {},

            "horizons": horizons
        }

        # --------------------------------------------------
        # TIMEFRAME METADATA
        # --------------------------------------------------

        for timeframe, df in candles.items():

            if df is None or df.empty:

                symbol_context[
                    "timeframes"
                ][timeframe] = {

                    "status": "NO_DATA",

                    "candles": 0
                }

                continue

            symbol_context[
                "timeframes"
            ][timeframe] = {

                "status": "READY",

                "candles": len(df),

                "start": (
                    df["time"].min()
                    .isoformat()
                ),

                "end": (
                    df["time"].max()
                    .isoformat()
                )
            }

        # --------------------------------------------------
        # STORE IN MEMORY
        # --------------------------------------------------

        self.context[symbol] = (
            symbol_context
        )

        # --------------------------------------------------
        # PERSIST HORIZONS
        # --------------------------------------------------

        for horizon, analysis in (
            horizons.items()
        ):

            if not isinstance(
                analysis,
                dict
            ):
                continue

            if analysis.get(
                "status"
            ) != "OK":
                continue

            result = self.store.save(
                symbol=symbol,
                horizon=horizon,
                context=analysis
            )

            if result.get(
                "status"
            ) == "REJECTED":

                print(
                    f"Context rejected: "
                    f"{symbol} {horizon}"
                )

                print(
                    result.get(
                        "errors"
                    )
                )

            else:

                print(
                    f"Stored: "
                    f"{symbol} {horizon}"
                )

        return symbol_context

    # ==================================================
    # BUILD ALL
    # ==================================================

    def build_all(self):

        results = {}

        for symbol in get_symbols():

            try:

                results[symbol] = (
                    self.build_symbol_context(
                        symbol
                    )
                )

            except Exception as error:

                results[symbol] = {

                    "symbol": symbol,

                    "status": "ERROR",

                    "error": str(error)
                }

        return results

    # ==================================================
    # GET
    # ==================================================

    def get(
        self,
        symbol
    ):

        return self.context.get(
            symbol.upper()
        )

    # ==================================================
    # GET TIMEFRAME
    # ==================================================

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
            timeframe.upper()
        )

    # ==================================================
    # STATUS
    # ==================================================

    def status(self):

        output = {}

        for symbol, context in (
            self.context.items()
        ):

            output[symbol] = {

                "created_at":
                    context.get(
                        "created_at"
                    ),

                "timeframes": {},

                "horizons": {}
            }

            for timeframe, data in (
                context[
                    "timeframes"
                ].items()
            ):

                output[symbol][
                    "timeframes"
                ][timeframe] = data

            for horizon, data in (
                context[
                    "horizons"
                ].items()
            ):

                output[symbol][
                    "horizons"
                ][horizon] = {

                    "status":
                        data.get(
                            "status"
                        ),

                    "direction":
                        data.get(
                            "direction"
                        ),

                    "bars":
                        data.get(
                            "bars",
                            0
                        )
                }

        return output