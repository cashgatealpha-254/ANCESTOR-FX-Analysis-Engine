from environment.context_schema import ContextSchema


class ContextValidator:

    REQUIRED_FIELDS = {
        "symbol",
        "horizon",
        "direction",
        "trend",
        "smc",
        "liquidity",
        "market_profile",
        "location",
        "relevant_zones",
        "confluence"
    }

    VALID_HORIZONS = {
        "SWING",
        "INTRADAY",
        "SCALPING"
    }

    VALID_DIRECTIONS = {
        "BULLISH",
        "BEARISH",
        "NEUTRAL"
    }

    def validate(
        self,
        context
    ):

        errors = []

        if not isinstance(
            context,
            dict
        ):

            return {
                "valid": False,
                "errors": [
                    "Context must be a dictionary"
                ]
            }

        missing = (
            self.REQUIRED_FIELDS
            - set(context.keys())
        )

        if missing:

            errors.append({
                "type": "MISSING_FIELDS",
                "fields": sorted(missing)
            })

        horizon = str(
            context.get(
                "horizon",
                ""
            )
        ).upper()

        if horizon not in self.VALID_HORIZONS:

            errors.append({
                "type": "INVALID_HORIZON",
                "value": horizon
            })

        direction = str(
            context.get(
                "direction",
                ""
            )
        ).upper()

        if direction not in self.VALID_DIRECTIONS:

            errors.append({
                "type": "INVALID_DIRECTION",
                "value": direction
            })

        return {

            "valid": not errors,

            "schema_version": (
                ContextSchema.VERSION
            ),

            "errors": errors
        }