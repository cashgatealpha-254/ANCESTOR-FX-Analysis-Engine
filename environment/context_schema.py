class ContextSchema:

    VERSION = "1.0"

    @staticmethod
    def build(
        symbol,
        horizon,
        context
    ):

        return {

            "schema_version": (
                ContextSchema.VERSION
            ),

            "symbol": symbol,

            "horizon": horizon,

            "analysis_time": (
                context.get("analysis_time")
            ),

            "timeframe": (
                context.get("timeframe")
            ),

            "bars": (
                context.get("bars")
            ),

            # ==========================================
            # MARKET STATE
            # ==========================================

            "direction": (
                context.get("direction")
            ),

            "trend": (
                context.get("trend")
            ),

            "smc": (
                context.get("smc")
            ),

            "liquidity": (
                context.get("liquidity")
            ),

            # ==========================================
            # LOCATION
            # ==========================================

            "supply_demand": (
                context.get("supply_demand")
            ),

            "market_profile": (
                context.get("market_profile")
            ),

            "location": (
                context.get("location")
            ),

            # ==========================================
            # ZONES
            # ==========================================

            "fvg": (
                context.get("fvg")
            ),

            "order_blocks": (
                context.get("order_blocks")
            ),

            "relevant_zones": (
                context.get("relevant_zones")
            ),

            # ==========================================
            # CONFLUENCE
            # ==========================================

            "confluence": (
                context.get("confluence")
            )
        }