# environment/horizon_engine.py

import pandas as pd

from environment.trend_engine import TrendEngine
from environment.supply_demand_engine import SupplyDemandEngine
from environment.market_profile_engine import MarketProfileEngine
from environment.smc_engine import SMCEngine
from environment.liquidity_engine import LiquidityEngine
from environment.fvg_engine import FVGEngine
from environment.order_block_engine import OrderBlockEngine
from environment.location_engine import LocationEngine
from environment.confluence_engine import ConfluenceEngine
from environment.zone_relevance import ZoneRelevance


class HorizonEngine:

    def __init__(self):

        self.trend_engine = TrendEngine()
        self.supply_demand_engine = SupplyDemandEngine()
        self.market_profile_engine = MarketProfileEngine()
        self.smc_engine = SMCEngine()
        self.liquidity_engine = LiquidityEngine()
        self.fvg_engine = FVGEngine()
        self.order_block_engine = OrderBlockEngine()

        self.location_engine = LocationEngine()
        self.confluence_engine = ConfluenceEngine()

        self.zone_relevance = ZoneRelevance(
            max_zones=3
        )

    # ==================================================
    # ANALYZE ONE HORIZON
    # ==================================================

    def analyze(
        self,
        symbol,
        horizon,
        timeframe,
        candles
    ):

        symbol = symbol.upper()
        horizon = horizon.upper()
        timeframe = timeframe.upper()

        if candles is None:

            return {
                "status": "NO_DATA",
                "symbol": symbol,
                "horizon": horizon,
                "timeframe": timeframe,
                "bars": 0
            }

        if not isinstance(
            candles,
            pd.DataFrame
        ):

            return {
                "status": "ERROR",
                "symbol": symbol,
                "horizon": horizon,
                "timeframe": timeframe,
                "bars": 0,
                "error": "Candles must be a pandas DataFrame"
            }

        if candles.empty:

            return {
                "status": "NO_DATA",
                "symbol": symbol,
                "horizon": horizon,
                "timeframe": timeframe,
                "bars": 0
            }

        df = candles.copy()

        # --------------------------------------------------
        # NORMALIZE TIME
        # --------------------------------------------------

        if "time" in df.columns:

            df["time"] = pd.to_datetime(
                df["time"]
            )

        # ==================================================
        # ENVIRONMENTAL INTELLIGENCE
        # ==================================================

        trend = self._safe_analyze(
            self.trend_engine.analyze,
            df
        )

        supply_demand = self._safe_analyze(
            self.supply_demand_engine.analyze,
            df
        )

        market_profile = self._safe_analyze(
            self.market_profile_engine.analyze,
            df
        )

        smc = self._safe_analyze(
            self.smc_engine.analyze,
            df
        )

        liquidity = self._safe_analyze(
            self.liquidity_engine.analyze,
            df
        )

        fvg = self._safe_analyze(
            self.fvg_engine.analyze,
            df
        )

        order_blocks = self._safe_analyze(
            self.order_block_engine.analyze,
            df
        )

        # ==================================================
        # DIRECTION
        # ==================================================

        direction = self._get_direction(
            trend,
            smc
        )

        # ==================================================
        # RELEVANT ZONES
        # ==================================================

        relevant_zones = self._safe_analyze(
            self.zone_relevance.analyze,
            direction=direction,
            fvg=fvg,
            order_blocks=order_blocks,
            profile=market_profile
        )

        # ==================================================
        # LOCATION
        # ==================================================

        location = self._safe_analyze(
            self.location_engine.analyze,
            df,
            supply_demand=supply_demand,
            market_profile=market_profile,
            fvg=(
                relevant_zones.get(
                    "fvg",
                    []
                )
                if isinstance(
                    relevant_zones,
                    dict
                )
                else []
            ),
            order_blocks=(
                relevant_zones.get(
                    "order_blocks",
                    []
                )
                if isinstance(
                    relevant_zones,
                    dict
                )
                else []
            )
        )

        # ==================================================
        # CONFLUENCE
        # ==================================================

        confluence = self._safe_analyze(
            self.confluence_engine.analyze,
            direction,
            trend,
            smc,
            liquidity,
            location,
            (
                relevant_zones.get(
                    "fvg",
                    []
                )
                if isinstance(
                    relevant_zones,
                    dict
                )
                else []
            ),
            (
                relevant_zones.get(
                    "order_blocks",
                    []
                )
                if isinstance(
                    relevant_zones,
                    dict
                )
                else []
            )
        )

        # ==================================================
        # SNAPSHOT
        # ==================================================

        return {

            "status": "OK",

            "symbol": symbol,

            "horizon": horizon,

            "timeframe": timeframe,

            "bars": len(df),

            "analysis_time": (
                pd.Timestamp.now().isoformat()
            ),

            "direction": direction,

            "trend": trend,

            "supply_demand": supply_demand,

            "market_profile": market_profile,

            "smc": smc,

            "liquidity": liquidity,

            "fvg": fvg,

            "order_blocks": order_blocks,

            "relevant_zones": relevant_zones,

            "location": location,

            "confluence": confluence
        }

    # ==================================================
    # ANALYZE ALL HORIZONS
    # ==================================================

    def analyze_context(
        self,
        symbol,
        context
    ):

        results = {}

        horizon_map = {

            "SWING": "H4",

            "INTRADAY": "M15",

            "SCALPING": "M5"
        }

        for horizon, timeframe in (
            horizon_map.items()
        ):

            candles = context.get(
                timeframe
            )

            results[horizon] = self.analyze(
                symbol=symbol,
                horizon=horizon,
                timeframe=timeframe,
                candles=candles
            )

        return results

    # ==================================================
    # DIRECTION
    # ==================================================

    @staticmethod
    def _get_direction(
        trend,
        smc
    ):

        trend_direction = "NEUTRAL"

        if isinstance(
            trend,
            dict
        ):

            trend_direction = str(
                trend.get(
                    "trend",
                    ""
                )
            ).upper()

            if trend_direction not in {
                "BULLISH",
                "BEARISH"
            }:

                trend_direction = "NEUTRAL"

        bullish_structure = 0
        bearish_structure = 0

        if isinstance(
            smc,
            dict
        ):

            structure = smc.get(
                "structure",
                []
            )

            for item in structure[-6:]:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                structure_type = str(
                    item.get(
                        "type",
                        ""
                    )
                ).upper()

                if structure_type in {
                    "HH",
                    "HL"
                }:

                    bullish_structure += 1

                elif structure_type in {
                    "LH",
                    "LL"
                }:

                    bearish_structure += 1

        if bullish_structure > bearish_structure:

            if trend_direction in {
                "BULLISH",
                "NEUTRAL"
            }:

                return "BULLISH"

        if bearish_structure > bullish_structure:

            if trend_direction in {
                "BEARISH",
                "NEUTRAL"
            }:

                return "BEARISH"

        return trend_direction

    # ==================================================
    # SAFE ANALYZE
    # ==================================================

    @staticmethod
    def _safe_analyze(
        engine,
        *args,
        **kwargs
    ):

        try:

            return engine(
                *args,
                **kwargs
            )

        except Exception as error:

            return {
                "status": "ERROR",
                "error": str(error)
            }