class ContextAdapter:

    def build(
        self,
        deep_context,
        recent_context,
        changes
    ):

        if deep_context is None:

            return {
                "status": "NO_DEEP_CONTEXT",
                "deep_context": None,
                "recent_context": recent_context,
                "changes": changes
            }

        if recent_context is None:

            return {
                "status": "NO_RECENT_CONTEXT",
                "deep_context": deep_context,
                "recent_context": None,
                "changes": changes
            }

        return {

            "status": "OK",

            # ==========================================
            # IDENTITY
            # ==========================================

            "symbol": deep_context.get(
                "symbol"
            ),

            "horizon": deep_context.get(
                "horizon"
            ),

            "context_version": deep_context.get(
                "context_version"
            ),

            "deep_analysis_time": deep_context.get(
                "analysis_time"
            ),

            # ==========================================
            # DEEP CONTEXT
            # ==========================================

            "deep_context": {

                "direction": deep_context.get(
                    "direction"
                ),

                "trend": deep_context.get(
                    "trend"
                ),

                "market_structure": deep_context.get(
                    "smc"
                ),

                "liquidity": deep_context.get(
                    "liquidity"
                ),

                "location": deep_context.get(
                    "location"
                ),

                "confluence": deep_context.get(
                    "confluence"
                ),

                "market_profile": deep_context.get(
                    "market_profile"
                ),

                "relevant_zones": deep_context.get(
                    "relevant_zones"
                )
            },

            # ==========================================
            # RECENT CONTEXT
            # ==========================================

            "recent_context": {

                "start_time": recent_context.get(
                    "start_time"
                ),

                "end_time": recent_context.get(
                    "end_time"
                ),

                "latest_close": recent_context.get(
                    "latest_close"
                ),

                "bars": recent_context.get(
                    "bars"
                ),

                "timeframe": recent_context.get(
                    "timeframe"
                )
            },

            # ==========================================
            # CHANGES
            # ==========================================

            "changes": changes
        }