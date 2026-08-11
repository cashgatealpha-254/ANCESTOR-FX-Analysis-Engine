from environment.context_schema import ContextSchema
from environment.context_validator import ContextValidator
from environment.deep_context_store import DeepContextStore


class DeepContextRecorder:

    def __init__(self):

        self.store = DeepContextStore()
        self.validator = ContextValidator()

    # ==================================================
    # RECORD HORIZON RESULTS
    # ==================================================

    def record(
        self,
        symbol,
        horizon_results
    ):

        if not isinstance(
            horizon_results,
            dict
        ):

            return {
                "status": "ERROR",
                "symbol": symbol,
                "recorded": 0,
                "errors": [
                    "Horizon results must be a dictionary"
                ]
            }

        recorded = []
        rejected = []

        for horizon, raw_context in (
            horizon_results.items()
        ):

            # ------------------------------------------
            # ONLY RECORD SUCCESSFUL ANALYSIS
            # ------------------------------------------

            if not isinstance(
                raw_context,
                dict
            ):

                rejected.append({
                    "horizon": horizon,
                    "reason": "Invalid context type"
                })

                continue

            if raw_context.get(
                "status"
            ) != "OK":

                rejected.append({
                    "horizon": horizon,
                    "reason": (
                        raw_context.get(
                            "status",
                            "UNKNOWN"
                        )
                    )
                })

                continue

            # ------------------------------------------
            # NORMALIZE
            # ------------------------------------------

            normalized = ContextSchema.build(
                symbol=symbol,
                horizon=horizon,
                context=raw_context
            )

            # ------------------------------------------
            # VALIDATE
            # ------------------------------------------

            validation = self.validator.validate(
                normalized
            )

            if not validation["valid"]:

                rejected.append({
                    "horizon": horizon,
                    "reason": "VALIDATION_FAILED",
                    "errors": validation["errors"]
                })

                continue

            # ------------------------------------------
            # STORE
            # ------------------------------------------

            result = self.store.save(
                symbol=symbol,
                horizon=horizon,
                context=raw_context
            )

            if result.get(
                "status"
            ) == "REJECTED":

                rejected.append({
                    "horizon": horizon,
                    "reason": "STORE_REJECTED",
                    "errors": result.get(
                        "errors",
                        []
                    )
                })

                continue

            recorded.append({
                "symbol": symbol,
                "horizon": horizon,
                "context_version": (
                    result.get(
                        "context_version"
                    )
                )
            })

        return {

            "status": "OK",

            "symbol": symbol,

            "recorded": len(recorded),

            "rejected": len(rejected),

            "contexts": recorded,

            "rejections": rejected
        }