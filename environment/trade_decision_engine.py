from environment.trade_setup_engine import TradeSetupEngine


class TradeDecisionEngine:

    def __init__(
        self,
        minimum_rr=2.0,
        max_setups=3
    ):

        self.trade_setup_engine = TradeSetupEngine(
            minimum_rr=minimum_rr
        )

        self.max_setups = int(
            max_setups
        )

    # ==================================================
    # BUILD TRADE DECISIONS
    # ==================================================

    def decide(
        self,
        opportunities,
        horizon_results=None,
        market=None
    ):

        if not isinstance(
            opportunities,
            list
        ):

            return []

        if not opportunities:

            return []

        decisions = []

        for opportunity in opportunities:

            if not isinstance(
                opportunity,
                dict
            ):

                continue

            # ------------------------------------------
            # CROSS-HORIZON FILTER
            # ------------------------------------------

            if not self._horizon_alignment_allows_trade(
                opportunity,
                horizon_results
            ):

                continue

            # ------------------------------------------
            # Rehydrate opportunity with horizon data
            # ------------------------------------------

            enriched = self._enrich_opportunity(
                opportunity,
                horizon_results
            )

            # ------------------------------------------
            # Build actual trade setup
            # ------------------------------------------

            setup = self.trade_setup_engine.build(
                enriched,
                market=market
            )

            if not isinstance(
                setup,
                dict
            ):

                continue

            # ------------------------------------------
            # Preserve opportunity metadata
            # ------------------------------------------

            setup["opportunity"] = enriched

            decisions.append(
                setup
            )

        # ----------------------------------------------
        # Highest-quality trade candidates first
        # ----------------------------------------------

        decisions.sort(
            key=self._decision_priority,
            reverse=True
        )

        return decisions[
            :self.max_setups
        ]

    # ==================================================
    # CROSS-HORIZON ALIGNMENT
    # ==================================================

    @staticmethod
    def _horizon_alignment_allows_trade(
        opportunity,
        horizon_results
    ):

        if not isinstance(
            horizon_results,
            dict
        ):

            return True

        direction = str(
            opportunity.get(
                "direction",
                ""
            )
        ).upper()

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return False

        swing = horizon_results.get(
            "SWING",
            {}
        )

        intraday = horizon_results.get(
            "INTRADAY",
            {}
        )

        scalping = horizon_results.get(
            "SCALPING",
            {}
        )

        if not all(
            isinstance(
                context,
                dict
            )
            for context in (
                swing,
                intraday,
                scalping
            )
        ):

            return False

        swing_direction = str(
            swing.get(
                "direction",
                "NEUTRAL"
            )
        ).upper()

        intraday_direction = str(
            intraday.get(
                "direction",
                "NEUTRAL"
            )
        ).upper()

        scalping_direction = str(
            scalping.get(
                "direction",
                "NEUTRAL"
            )
        ).upper()

        # ------------------------------------------
        # Higher timeframe bias
        # ------------------------------------------

        if swing_direction != direction:

            return False

        # ------------------------------------------
        # Intraday must not oppose the trade
        # ------------------------------------------

        if intraday_direction not in {
            "NEUTRAL",
            direction
        }:

            return False

        # ------------------------------------------
        # Scalping must agree with execution
        # ------------------------------------------

        if scalping_direction != direction:

            return False

        return True

    # ==================================================
    # REHYDRATE OPPORTUNITY
    # ==================================================

    @staticmethod
    def _enrich_opportunity(
        opportunity,
        horizon_results
    ):

        enriched = dict(
            opportunity
        )

        if not isinstance(
            horizon_results,
            dict
        ):

            return enriched

        horizon = opportunity.get(
            "horizon"
        )

        horizon_data = horizon_results.get(
            horizon
        )

        if not isinstance(
            horizon_data,
            dict
        ):

            return enriched

        # ------------------------------------------
        # Copy environmental intelligence
        # ------------------------------------------

        for key in (
            "trend",
            "supply_demand",
            "market_profile",
            "smc",
            "liquidity",
            "fvg",
            "order_blocks",
            "location",
            "confluence"
        ):

            if (
                key not in enriched
                or enriched.get(key) is None
            ):

                if key in horizon_data:

                    enriched[key] = (
                        horizon_data.get(key)
                    )

        # ------------------------------------------
        # Direction
        # ------------------------------------------

        if (
            enriched.get("direction")
            in {
                None,
                "",
                "NEUTRAL"
            }
        ):

            enriched["direction"] = (
                horizon_data.get(
                    "direction"
                )
            )

        # ------------------------------------------
        # Symbol
        # ------------------------------------------

        if not enriched.get(
            "symbol"
        ):

            enriched["symbol"] = (
                horizon_data.get(
                    "symbol"
                )
            )

        # ------------------------------------------
        # Horizon
        # ------------------------------------------

        if not enriched.get(
            "horizon"
        ):

            enriched["horizon"] = (
                horizon_data.get(
                    "horizon"
                )
            )

        # ------------------------------------------
        # Relevant zones
        # ------------------------------------------

        if not isinstance(
            enriched.get(
                "relevant_zones"
            ),
            dict
        ):

            location = enriched.get(
                "location"
            )

            if isinstance(
                location,
                dict
            ):

                enriched[
                    "relevant_zones"
                ] = {

                    "fvg":
                        location.get(
                            "fvg",
                            []
                        ),

                    "order_blocks":
                        location.get(
                            "order_blocks",
                            []
                        )
                }

        return enriched

    # ==================================================
    # DECISION PRIORITY
    # ==================================================

    @staticmethod
    def _decision_priority(
        setup
    ):

        status = str(
            setup.get(
                "status",
                ""
            )
        ).upper()

        score = float(
            setup.get(
                "score",
                0
            ) or 0
        )

        rr = float(
            setup.get(
                "rr",
                0
            ) or 0
        )

        status_priority = {

            "READY": 3,

            "WAITING": 2,

            "REJECTED": 1,

            "ERROR": 0,

            "BLOCKED": 0

        }.get(
            status,
            0
        )

        return (
            status_priority,
            score,
            rr
        )