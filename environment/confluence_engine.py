class ConfluenceEngine:

    def analyze(
        self,
        direction,
        trend,
        smc,
        liquidity,
        location,
        fvg,
        order_blocks
    ):
        """
        Determine whether environmental signals
        agree with the current directional bias.
        """

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return {
                "direction": "NEUTRAL",
                "score": 0,
                "signals": [],
                "conflicts": []
            }

        signals = []
        conflicts = []

        score = 0

        # --------------------------------
        # Trend alignment
        # --------------------------------

        if isinstance(trend, dict):

            trend_value = str(
                trend.get(
                    "direction",
                    ""
                )
            ).upper()

            if trend_value == direction:

                score += 15

                signals.append(
                    f"{direction.lower()} trend aligned"
                )

            elif trend_value in {
                "BULLISH",
                "BEARISH"
            }:

                score -= 10

                conflicts.append(
                    "trend conflicts with direction"
                )

        # --------------------------------
        # SMC structure
        # --------------------------------

        if isinstance(smc, dict):

            breaks = smc.get(
                "structure_breaks",
                []
            )

            if breaks:

                latest = breaks[-1]

                structure_direction = str(
                    latest.get(
                        "direction",
                        ""
                    )
                ).upper()

                if structure_direction == direction:

                    score += 20

                    signals.append(
                        f"{direction.lower()} "
                        f"{latest.get('type')} confirmation"
                    )

                elif structure_direction in {
                    "BULLISH",
                    "BEARISH"
                }:

                    score -= 15

                    conflicts.append(
                        "SMC structure conflict"
                    )

        # --------------------------------
        # Liquidity
        # --------------------------------

        if isinstance(liquidity, dict):

            buy_side = liquidity.get(
                "buy_side",
                []
            )

            sell_side = liquidity.get(
                "sell_side",
                []
            )

            if buy_side:

                if direction == "BULLISH":

                    score += 5

                    signals.append(
                        "buy-side liquidity available"
                    )

            if sell_side:

                if direction == "BEARISH":

                    score += 5

                    signals.append(
                        "sell-side liquidity available"
                    )

        # --------------------------------
        # Location
        # --------------------------------

        if isinstance(location, dict):

            nearby = location.get(
                "nearby_zones",
                []
            )

            for zone in nearby:

                zone_direction = str(
                    zone.get(
                        "direction",
                        ""
                    )
                ).upper()

                zone_type = zone.get(
                    "type",
                    "ZONE"
                )

                if zone_direction == direction:

                    score += 10

                    signals.append(
                        f"{zone_type} aligned with direction"
                    )

                elif zone_direction in {
                    "BULLISH",
                    "BEARISH"
                }:

                    score -= 5

                    conflicts.append(
                        f"{zone_type} conflicts with direction"
                    )

        # --------------------------------
        # FVG
        # --------------------------------

        if isinstance(fvg, dict):

            if direction == "BULLISH":

                if fvg.get("bullish"):

                    score += 10

                    signals.append(
                        "bullish FVG available"
                    )

                if fvg.get("bearish"):

                    conflicts.append(
                        "bearish FVG also present"
                    )

            elif direction == "BEARISH":

                if fvg.get("bearish"):

                    score += 10

                    signals.append(
                        "bearish FVG available"
                    )

                if fvg.get("bullish"):

                    conflicts.append(
                        "bullish FVG also present"
                    )

        # --------------------------------
        # Order blocks
        # --------------------------------

        if isinstance(order_blocks, dict):

            aligned_blocks = (
                order_blocks.get(
                    "bullish"
                    if direction == "BULLISH"
                    else "bearish",
                    []
                )
            )

            if aligned_blocks:

                score += 10

                signals.append(
                    f"{direction.lower()} "
                    "order-block available"
                )

        # --------------------------------
        # Final score
        # --------------------------------

        score = max(
            0,
            min(score, 100)
        )

        return {
            "direction": direction,
            "score": score,
            "signals": signals,
            "conflicts": conflicts
        }