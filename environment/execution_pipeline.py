from environment.setup_validator import SetupValidator
from environment.risk_engine import RiskEngine
from environment.position_sizer import PositionSizer
from environment.execution_engine import ExecutionEngine


class ExecutionPipeline:

    def __init__(
        self,
        risk_percent=1.0,
        max_risk_percent=2.0,
        minimum_rr=2.0,
        max_positions=1,
        dry_run=True
    ):

        self.setup_validator = SetupValidator(
            minimum_rr=minimum_rr,
            minimum_zone_ticks=2.0,
            minimum_stop_ticks=2.0
        )

        self.risk_engine = RiskEngine(
            risk_percent=risk_percent,
            max_risk_percent=max_risk_percent,
            minimum_rr=minimum_rr
        )

        self.position_sizer = PositionSizer(
            risk_percent=risk_percent
        )

        self.execution_engine = ExecutionEngine(
            max_positions=max_positions,
            dry_run=dry_run
        )

    # ==================================================
    # RUN PIPELINE
    # ==================================================

    def execute(
        self,
        setup
    ):

        if not isinstance(
            setup,
            dict
        ):

            return {
                "status": "BLOCKED",
                "stage": "SETUP_VALIDATION",
                "reason": "Invalid setup"
            }

        # ==================================================
        # STEP 1 — SETUP VALIDATION
        # ==================================================

        validation = self.setup_validator.validate(
            setup
        )

        if validation.get(
            "status"
        ) != "READY":

            return {

                "status": "BLOCKED",

                "stage": "SETUP_VALIDATION",

                "symbol": setup.get(
                    "symbol"
                ),

                "direction": setup.get(
                    "direction"
                ),

                "horizon": setup.get(
                    "horizon"
                ),

                "score": setup.get(
                    "score"
                ),

                "validation": validation,

                "reason": validation.get(
                    "reason",
                    "Setup validation failed"
                )
            }

        # ==================================================
        # MERGE VALIDATION
        # ==================================================

        enriched_setup = {
            **setup,
            **validation
        }

        # ==================================================
        # STEP 2 — RISK VALIDATION
        # ==================================================

        risk = self.risk_engine.validate(
            enriched_setup
        )

        if risk.get(
            "status"
        ) != "ALLOW":

            return {

                "status": "BLOCKED",

                "stage": "RISK",

                "symbol": enriched_setup.get(
                    "symbol"
                ),

                "direction": enriched_setup.get(
                    "direction"
                ),

                "horizon": enriched_setup.get(
                    "horizon"
                ),

                "score": enriched_setup.get(
                    "score"
                ),

                "validation": validation,

                "risk": risk,

                "reason": risk.get(
                    "reason",
                    "Risk validation failed"
                )
            }

        # ==================================================
        # MERGE RISK
        # ==================================================

        enriched_setup.update(
            risk
        )

        # ==================================================
        # STEP 3 — POSITION SIZING
        # ==================================================

        sizing = self.position_sizer.calculate(
            enriched_setup
        )

        if sizing.get(
            "status"
        ) != "READY":

            return {

                "status": "BLOCKED",

                "stage": "POSITION_SIZE",

                "symbol": enriched_setup.get(
                    "symbol"
                ),

                "direction": enriched_setup.get(
                    "direction"
                ),

                "horizon": enriched_setup.get(
                    "horizon"
                ),

                "score": enriched_setup.get(
                    "score"
                ),

                "validation": validation,

                "risk": risk,

                "sizing": sizing,

                "reason": sizing.get(
                    "reason",
                    "Position sizing failed"
                )
            }

        # ==================================================
        # MERGE POSITION SIZE
        # ==================================================

        enriched_setup.update(
            sizing
        )

        # ==================================================
        # STEP 4 — EXECUTION
        # ==================================================

        execution = self.execution_engine.execute(
            enriched_setup
        )

        # ==================================================
        # FINAL RESULT
        # ==================================================

        return {

            "status": execution.get(
                "status",
                "UNKNOWN"
            ),

            "stage": "EXECUTION",

            "symbol": enriched_setup.get(
                "symbol"
            ),

            "direction": enriched_setup.get(
                "direction"
            ),

            "horizon": enriched_setup.get(
                "horizon"
            ),

            "score": enriched_setup.get(
                "score"
            ),

            "entry": enriched_setup.get(
                "entry"
            ),

            "stop_loss": enriched_setup.get(
                "stop_loss"
            ),

            "take_profit": enriched_setup.get(
                "take_profit"
            ),

            "rr": enriched_setup.get(
                "rr"
            ),

            "validation": validation,

            "risk": risk,

            "sizing": sizing,

            "execution": execution
        }