class OpportunitySelector:

    def __init__(
        self,
        minimum_score=70,
        max_opportunities=3
    ):

        self.minimum_score = minimum_score
        self.max_opportunities = max_opportunities

    # ==================================================
    # SELECT
    # ==================================================

    def select(
        self,
        opportunities
    ):

        if not isinstance(
            opportunities,
            list
        ):

            return []

        valid = []

        for opportunity in opportunities:

            if not isinstance(
                opportunity,
                dict
            ):

                continue

            score = opportunity.get(
                "score",
                0
            )

            try:

                score = float(score)

            except (
                TypeError,
                ValueError
            ):

                continue

            # ------------------------------------------
            # Minimum quality threshold
            # ------------------------------------------

            if score < self.minimum_score:

                continue

            # ------------------------------------------
            # Direction must be actionable
            # ------------------------------------------

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

                continue

            valid.append(
                opportunity
            )

        # ----------------------------------------------
        # Highest probability first
        # ----------------------------------------------

        valid.sort(
            key=lambda item: float(
                item.get(
                    "score",
                    0
                )
            ),
            reverse=True
        )

        # ----------------------------------------------
        # Avoid duplicate symbol/horizon combinations
        # ----------------------------------------------

        selected = []

        seen = set()

        for opportunity in valid:

            key = (
                opportunity.get(
                    "symbol"
                ),
                opportunity.get(
                    "horizon"
                )
            )

            if key in seen:

                continue

            seen.add(key)

            selected.append(
                opportunity
            )

            if len(
                selected
            ) >= self.max_opportunities:

                break

        return selected