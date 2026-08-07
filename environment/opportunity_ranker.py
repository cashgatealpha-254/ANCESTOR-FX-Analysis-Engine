class OpportunityRanker:

    def __init__(self):

        self.weights = {
            "direction": 25,
            "location": 20,
            "liquidity": 15,
            "structure": 20,
            "imbalance": 15,
            "horizon": 5,
        }

    def rank(self, horizon_results):

        opportunities = []

        for horizon, data in horizon_results.items():

            if data.get("status") != "OK":
                continue

            direction_score, direction, direction_reasons = (
                self._score_direction(
                    data.get("trend"),
                    data.get("smc")
                )
            )

            location_score, location_reasons = (
                self._score_location(
                    data.get("location")
                )
            )

            liquidity_score, liquidity_reasons = (
                self._score_liquidity(
                    data.get("liquidity")
                )
            )

            structure_score, structure_reasons = (
                self._score_structure(
                    data.get("smc")
                )
            )

            imbalance_score, imbalance_reasons = (
                self._score_imbalance(
                    data.get("fvg"),
                    data.get("order_blocks")
                )
            )

            score = (
                direction_score
                + location_score
                + liquidity_score
                + structure_score
                + imbalance_score
                + self.weights["horizon"]
            )

            reasons = (
                direction_reasons
                + location_reasons
                + liquidity_reasons
                + structure_reasons
                + imbalance_reasons
                + [f"{horizon.lower()} horizon analyzed"]
            )

            opportunities.append({
                "symbol": data.get("symbol"),
                "horizon": horizon,
                "direction": direction,
                "score": min(score, 100),
                "location_score": location_score,
                "reasons": reasons,
            })

        opportunities.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return opportunities

    def _score_direction(self, trend, smc):

        bullish = 0
        bearish = 0
        reasons = []

        if isinstance(trend, dict):

            trend_value = str(
                trend.get("trend", "")
            ).upper()

            if trend_value == "BULLISH":
                bullish += 12
                reasons.append("bullish trend")

            elif trend_value == "BEARISH":
                bearish += 12
                reasons.append("bearish trend")

        if isinstance(smc, dict):

            structure = smc.get(
                "structure",
                []
            )

            bullish_structure = 0
            bearish_structure = 0

            for item in structure[-6:]:

                structure_type = item.get("type")

                if structure_type in {"HH", "HL"}:
                    bullish_structure += 1

                elif structure_type in {"LH", "LL"}:
                    bearish_structure += 1

            if bullish_structure > bearish_structure:

                bullish += 13
                reasons.append(
                    "bullish market structure"
                )

            elif bearish_structure > bullish_structure:

                bearish += 13
                reasons.append(
                    "bearish market structure"
                )

        if bullish > bearish:

            return (
                min(
                    bullish,
                    self.weights["direction"]
                ),
                "BULLISH",
                reasons
            )

        if bearish > bullish:

            return (
                min(
                    bearish,
                    self.weights["direction"]
                ),
                "BEARISH",
                reasons
            )

        return (
            0,
            "NEUTRAL",
            ["directional conflict"]
        )

    def _score_location(self, location):

        if not isinstance(location, dict):
            return 0, []

        score = location.get(
            "score",
            0
        )

        nearby = location.get(
            "nearby_zones",
            []
        )

        reasons = []

        for zone in nearby:

            zone_type = zone.get(
                "type",
                "UNKNOWN"
            )

            distance = zone.get(
                "distance_pct"
            )

            if distance is not None:

                reasons.append(
                    f"{zone_type} nearby "
                    f"({distance:.2f}%)"
                )

            else:

                reasons.append(
                    f"{zone_type} nearby"
                )

        if not nearby:

            reasons.append(
                "no nearby actionable zones"
            )

        return (
            min(
                int(score),
                self.weights["location"]
            ),
            reasons
        )

    def _score_liquidity(self, liquidity):

        score = 0
        reasons = []

        if not isinstance(liquidity, dict):
            return 0, reasons

        buy_side = liquidity.get(
            "buy_side",
            []
        )

        sell_side = liquidity.get(
            "sell_side",
            []
        )

        if buy_side:

            score += 7
            reasons.append(
                "buy-side liquidity identified"
            )

        if sell_side:

            score += 8
            reasons.append(
                "sell-side liquidity identified"
            )

        return (
            min(
                score,
                self.weights["liquidity"]
            ),
            reasons
        )

    def _score_structure(self, smc):

        score = 0
        reasons = []

        if not isinstance(smc, dict):
            return 0, reasons

        breaks = smc.get(
            "structure_breaks",
            []
        )

        if not breaks:
            return 0, reasons

        latest = breaks[-1]

        direction = str(
            latest.get(
                "direction",
                ""
            )
        ).upper()

        structure_type = latest.get(
            "type"
        )

        if structure_type == "BOS":

            score += 15
            reasons.append(
                f"{direction.lower()} BOS"
            )

        elif structure_type == "CHoCH":

            score += 15
            reasons.append(
                f"{direction.lower()} CHoCH"
            )

        return (
            min(
                score,
                self.weights["structure"]
            ),
            reasons
        )

    def _score_imbalance(self, fvg, order_blocks):

        score = 0
        reasons = []

        if isinstance(fvg, dict):

            bullish = fvg.get(
                "bullish",
                []
            )

            bearish = fvg.get(
                "bearish",
                []
            )

            if bullish:

                score += 7
                reasons.append(
                    "bullish FVG identified"
                )

            if bearish:

                score += 8
                reasons.append(
                    "bearish FVG identified"
                )

        if isinstance(order_blocks, dict):

            bullish = order_blocks.get(
                "bullish",
                []
            )

            bearish = order_blocks.get(
                "bearish",
                []
            )

            if bullish:

                score += 5
                reasons.append(
                    "bullish order-block candidate"
                )

            elif bearish:

                score += 5
                reasons.append(
                    "bearish order-block candidate"
                )

        return (
            min(
                score,
                self.weights["imbalance"]
            ),
            reasons
        )