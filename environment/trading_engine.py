from environment.market_scanner import MarketScanner
from environment.candle_cache import CandleCache
from environment.horizon_engine import HorizonEngine
from environment.opportunity_ranker import OpportunityRanker
from environment.opportunity_selector import OpportunitySelector
from environment.trade_decision_engine import TradeDecisionEngine
from environment.execution_pipeline import ExecutionPipeline


class TradingEngine:

    def __init__(
        self,
        minimum_score=70,
        max_opportunities=3,
        minimum_rr=2.0,
        risk_percent=1.0,
        max_risk_percent=2.0,
        max_positions=1,
        dry_run=True
    ):

        # ==================================================
        # MARKET INTELLIGENCE
        # ==================================================

        self.market_scanner = MarketScanner()

        self.candle_cache = CandleCache()

        self.horizon_engine = HorizonEngine()

        # ==================================================
        # OPPORTUNITY INTELLIGENCE
        # ==================================================

        self.opportunity_ranker = OpportunityRanker()

        self.opportunity_selector = OpportunitySelector(
            minimum_score=minimum_score,
            max_opportunities=max_opportunities
        )

        # ==================================================
        # TRADE DECISION
        # ==================================================

        self.trade_decision_engine = TradeDecisionEngine(
            minimum_rr=minimum_rr,
            max_setups=max_opportunities
        )

        # ==================================================
        # EXECUTION
        # ==================================================

        self.execution_pipeline = ExecutionPipeline(
            risk_percent=risk_percent,
            max_risk_percent=max_risk_percent,
            minimum_rr=minimum_rr,
            max_positions=max_positions,
            dry_run=dry_run
        )

    # ==================================================
    # RUN SINGLE SYMBOL
    # ==================================================

    def run(
        self,
        symbol
    ):

        symbol = str(
            symbol
        ).upper()

        # ==================================================
        # LOAD REAL MARKET CONTEXT
        # ==================================================

        try:

            context = (
                self.candle_cache.build_symbol_context(
                    symbol
                )
            )

        except Exception as error:

            return {

                "status": "ERROR",

                "symbol": symbol,

                "reason": (
                    "Market context loading failed"
                ),

                "error": str(
                    error
                )
            }

        # ==================================================
        # HORIZON ANALYSIS
        # ==================================================

        try:

            horizon_results = (
                self.horizon_engine.analyze_context(
                    symbol=symbol,
                    context=context
                )
            )

        except Exception as error:

            return {

                "status": "ERROR",

                "symbol": symbol,

                "reason": (
                    "Horizon analysis failed"
                ),

                "error": str(
                    error
                )
            }

        if not isinstance(
            horizon_results,
            dict
        ):

            return {

                "status": "ERROR",

                "symbol": symbol,

                "reason": (
                    "Horizon analysis returned "
                    "invalid result"
                )
            }

        # ==================================================
        # RANK OPPORTUNITIES
        # ==================================================

        opportunities = (
            self.opportunity_ranker.rank(
                horizon_results
            )
        )

        if not isinstance(
            opportunities,
            list
        ):

            opportunities = []

        # ==================================================
        # SELECT BEST OPPORTUNITIES
        # ==================================================

        selected = (
            self.opportunity_selector.select(
                opportunities
            )
        )

        if not isinstance(
            selected,
            list
        ):

            selected = []

        # ==================================================
        # BUILD TRADE DECISIONS
        # ==================================================

        decisions = (
            self.trade_decision_engine.decide(
                selected,
                horizon_results=horizon_results
            )
        )

        if not isinstance(
            decisions,
            list
        ):

            decisions = []

        # ==================================================
        # EXECUTION
        # ==================================================

        executions = []

        for decision in decisions:

            if not isinstance(
                decision,
                dict
            ):

                continue

            try:

                execution = (
                    self.execution_pipeline.execute(
                        decision
                    )
                )

                executions.append(
                    execution
                )

            except Exception as error:

                executions.append({

                    "status": "ERROR",

                    "stage": "EXECUTION",

                    "symbol": symbol,

                    "reason": str(
                        error
                    )
                })

        # ==================================================
        # FINAL RESULT
        # ==================================================

        return {

            "status": "OK",

            "symbol": symbol,

            "horizon_results":
                horizon_results,

            "opportunities":
                opportunities,

            "selected":
                selected,

            "decisions":
                decisions,

            "executions":
                executions
        }

    # ==================================================
    # RUN MULTIPLE SYMBOLS
    # ==================================================

    def run_many(
        self,
        symbols
    ):

        if not isinstance(
            symbols,
            (list, tuple)
        ):

            return {}

        results = {}

        for symbol in symbols:

            try:

                symbol = str(
                    symbol
                ).upper()

                results[symbol] = (
                    self.run(
                        symbol
                    )
                )

            except Exception as error:

                results[symbol] = {

                    "status": "ERROR",

                    "symbol": symbol,

                    "reason": str(
                        error
                    )
                }

        return results