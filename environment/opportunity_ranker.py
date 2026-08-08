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

        self.max_zone_distance = 0.50

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
                    data.get("location"),
                    direction
                )
            )

            liquidity_score, liquidity_reasons = (
                self._score_liquidity(
                    data.get("liquidity"),
                    direction
                )
            )

            structure_score, structure_reasons = (
                self._score_structure(
                    data.get("smc"),
                    direction
                )
            )

            imbalance_score, imbalance_reasons = (
                self._score_imbalance(
                    data.get("relevant_zones"),
                    direction
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
                "score": min(round(score), 100),
                "location_score": location_score,

                # Preserve intelligence for TradeSetupEngine
                "trend": data.get("trend"),
                "smc": data.get("smc"),
                "liquidity": data.get("liquidity"),
                "location": data.get("location"),
                "relevant_zones": data.get("relevant_zones"),

                "reasons": reasons,
            })

        opportunities.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return opportunities

    # ==================================================
    # LOCATION
    # ==================================================

    def _score_location(
        self,
        location,
        direction
    ):

        if not isinstance(
            location,
            dict
        ):

            return 0, []

        nearby = location.get(
            "nearby_zones",
            []
        )

        if not nearby:

            return (
                0,
                ["no nearby actionable zones"]
            )

        score = 0
        reasons = []

        best_distance = None

        for zone in nearby:

            distance = zone.get(
                "distance_pct"
            )

            if distance is None:
                continue

            if distance > self.max_zone_distance:
                continue

            if (
                best_distance is None
                or distance < best_distance
            ):

                best_distance = distance

            zone_type = str(
                zone.get(
                    "type",
                    "UNKNOWN"
                )
            ).upper()

            # Closer zones receive more weight.
            if distance <= 0.05:
                zone_score = 8

            elif distance <= 0.10:
                zone_score = 6

            elif distance <= 0.25:
                zone_score = 4

            else:
                zone_score = 2

            # Profile zones are context,
            # not primary entry zones.
            if zone_type.startswith(
                "PROFILE_"
            ):

                zone_score = min(
                    zone_score,
                    3
                )

            score += zone_score

            reasons.append(
                f"{zone_type} "
                f"{distance:.2f}% from price"
            )

        score = min(
            score,
            self.weights["location"]
        )

        if best_distance is not None:

            reasons.insert(
                0,
                f"best actionable zone "
                f"{best_distance:.2f}% away"
            )

        return score, reasons

    # ==================================================
    # LIQUIDITY
    # ==================================================

    def _score_liquidity(
        self,
        liquidity,
        direction
    ):

        if not isinstance(
            liquidity,
            dict
        ):

            return 0, []

        score = 0
        reasons = []

        buy_side = liquidity.get(
            "buy_side",
            []
        )

        sell_side = liquidity.get(
            "sell_side",
            []
        )

        if direction == "BULLISH":

            if buy_side:

                score += 15

                reasons.append(
                    "bullish liquidity objective identified"
                )

            elif sell_side:

                score += 5

                reasons.append(
                    "sell-side liquidity available"
                )

        elif direction == "BEARISH":

            if sell_side:

                score += 15

                reasons.append(
                    "bearish liquidity objective identified"
                )

            elif buy_side:

                score += 5

                reasons.append(
                    "buy-side liquidity available"
                )

        else:

            if buy_side:

                score += 5

                reasons.append(
                    "buy-side liquidity available"
                )

            if sell_side:

                score += 5

                reasons.append(
                    "sell-side liquidity available"
                )

        return (
            min(
                score,
                self.weights["liquidity"]
            ),
            reasons
        )

    # ==================================================
    # STRUCTURE
    # ==================================================

    def _score_structure(
        self,
        smc,
        direction
    ):

        if not isinstance(
            smc,
            dict
        ):

            return 0, []

        breaks = smc.get(
            "structure_breaks",
            []
        )

        if not breaks:

            return (
                0,
                ["no structural confirmation"]
            )

        latest = breaks[-1]

        structure_type = str(
            latest.get(
                "type",
                ""
            )
        ).upper()

        break_direction = str(
            latest.get(
                "direction",
                ""
            )
        ).upper()

        if break_direction != direction:

            return (
                5,
                ["structure conflicts with direction"]
            )

        if structure_type == "BOS":

            return (
                20,
                [
                    f"{direction.lower()} BOS confirmation"
                ]
            )

        if structure_type == "CHOCH":

            return (
                15,
                [
                    f"{direction.lower()} CHoCH confirmation"
                ]
            )

        return (
            5,
            ["structural information available"]
        )

    # ==================================================
    # IMBALANCE
    # ==================================================

    def _score_imbalance(
        self,
        relevant_zones,
        direction
    ):

        if not isinstance(
            relevant_zones,
            dict
        ):

            return (
                0,
                ["no relevant zones"]
            )

        score = 0
        reasons = []

        fvg = relevant_zones.get(
            "fvg",
            []
        )

        order_blocks = relevant_zones.get(
            "order_blocks",
            []
        )

        # ------------------------------------------
        # FVG
        # ------------------------------------------

        aligned_fvg = []

        for zone in fvg:

            zone_direction = str(
                zone.get(
                    "direction",
                    direction
                )
            ).upper()

            if zone_direction == direction:

                aligned_fvg.append(
                    zone
                )

        if aligned_fvg:

            score += 8

            reasons.append(
                "FVG aligned with direction"
            )

        # ------------------------------------------
        # ORDER BLOCK
        # ------------------------------------------

        aligned_ob = []

        for zone in order_blocks:

            zone_direction = str(
                zone.get(
                    "direction",
                    direction
                )
            ).upper()

            if zone_direction == direction:

                aligned_ob.append(
                    zone
                )

        if aligned_ob:

            score += 7

            reasons.append(
                "order block aligned with direction"
            )

        # ------------------------------------------
        # CONFLUENCE BONUS
        # ------------------------------------------

        if aligned_fvg and aligned_ob:

            score += 3

            reasons.append(
                "FVG + order-block confluence"
            )

        return (
            min(
                score,
                self.weights["imbalance"]
            ),
            reasons
        )