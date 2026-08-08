from environment.market_context import MarketContext


class TradeSetupEngine:

    def __init__(self, minimum_rr=2.0):

        self.minimum_rr = float(
            minimum_rr
        )

        self.market_context = MarketContext()

    # ==================================================
    # BUILD SETUP
    # ==================================================

    def build(
        self,
        opportunity,
        market=None
    ):

        if not isinstance(
            opportunity,
            dict
        ):

            return {
                "status": "ERROR",
                "reason": "Invalid opportunity"
            }

        symbol = opportunity.get(
            "symbol"
        )

        horizon = opportunity.get(
            "horizon"
        )

        direction = str(
            opportunity.get(
                "direction",
                ""
            )
        ).upper()

        score = opportunity.get(
            "score",
            0
        )

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return {
                "status": "REJECTED",
                "symbol": symbol,
                "horizon": horizon,
                "direction": direction,
                "score": score,
                "reason": "No actionable direction"
            }

        # ==================================================
        # MARKET CONTEXT
        # ==================================================

        if market is None:

            market = self.market_context.get(
                symbol
            )

        if not isinstance(
            market,
            dict
        ):

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "Invalid market context"
            }

        if market.get(
            "status"
        ) != "OK":

            return {
                "status": "WAITING",
                "symbol": symbol,
                "horizon": horizon,
                "direction": direction,
                "score": score,
                "reason": "Market data unavailable"
            }

        try:

            current_price = float(
                market.get(
                    "mid"
                )
            )

        except (
            TypeError,
            ValueError
        ):

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "Invalid market price"
            }

        # ==================================================
        # SELECT ENTRY ZONE
        # ==================================================

        zone = self._select_zone(
            opportunity
        )

        if zone is None:

            return {
                "status": "WAITING",
                "symbol": symbol,
                "horizon": horizon,
                "direction": direction,
                "score": score,
                "current_price": current_price,
                "reason": "No actionable entry zone"
            }

        # ==================================================
        # ENTRY
        # ==================================================

        entry = self._entry_price(
            zone
        )

        if entry is None:

            return {
                "status": "WAITING",
                "symbol": symbol,
                "horizon": horizon,
                "direction": direction,
                "score": score,
                "current_price": current_price,
                "zone": zone,
                "reason": "Entry price unavailable"
            }

        # ==================================================
        # STOP LOSS
        # ==================================================

        stop_loss = self._stop_loss(
            zone,
            direction
        )

        if stop_loss is None:

            return {
                "status": "WAITING",
                "symbol": symbol,
                "horizon": horizon,
                "direction": direction,
                "score": score,
                "current_price": current_price,
                "entry": entry,
                "zone": zone,
                "reason": "Invalidation unavailable"
            }

        # ==================================================
        # RISK
        # ==================================================

        risk = abs(
            entry - stop_loss
        )

        if risk <= 0:

            return {
                "status": "REJECTED",
                "symbol": symbol,
                "horizon": horizon,
                "direction": direction,
                "score": score,
                "reason": "Invalid risk distance"
            }

        # ==================================================
        # TRIGGER STATE
        # ==================================================

        trigger = self._get_trigger_state(
            current_price,
            zone,
            direction
        )

        # ==================================================
        # WAITING / INVALIDATED
        # ==================================================

        if trigger != "ENTRY_NOW":

            return {

                "status": "WAITING",

                "symbol": symbol,

                "horizon": horizon,

                "direction": direction,

                "score": score,

                "current_price": current_price,

                "entry": entry,

                "stop_loss": stop_loss,

                "zone": zone,

                "trigger": trigger,

                "execution": "MANUAL",

                "invalidation": self._invalidation(
                    zone,
                    direction
                )
            }

        # ==================================================
        # TAKE PROFIT
        # ==================================================

        take_profit = self._take_profit(
            opportunity,
            entry,
            risk,
            direction
        )

        if take_profit is None:

            return {

                "status": "WAITING",

                "symbol": symbol,

                "horizon": horizon,

                "direction": direction,

                "score": score,

                "current_price": current_price,

                "entry": entry,

                "stop_loss": stop_loss,

                "zone": zone,

                "trigger": "ENTRY_NOW",

                "execution": "MANUAL",

                "reason": (
                    "No valid liquidity target"
                )
            }

        # ==================================================
        # REWARD
        # ==================================================

        reward = abs(
            take_profit - entry
        )

        if reward <= 0:

            return {

                "status": "REJECTED",

                "symbol": symbol,

                "horizon": horizon,

                "direction": direction,

                "score": score,

                "reason": "Invalid reward distance"
            }

        # ==================================================
        # RISK / REWARD
        # ==================================================

        rr = reward / risk

        if rr < self.minimum_rr:

            return {

                "status": "REJECTED",

                "symbol": symbol,

                "horizon": horizon,

                "direction": direction,

                "score": score,

                "current_price": current_price,

                "entry": entry,

                "stop_loss": stop_loss,

                "take_profit": take_profit,

                "rr": round(
                    rr,
                    2
                ),

                "reason": (
                    f"RR {rr:.2f} below "
                    f"minimum {self.minimum_rr:.2f}"
                )
            }

        # ==================================================
        # READY SETUP
        # ==================================================

        return {

            "status": "READY",

            "symbol": symbol,

            "horizon": horizon,

            "direction": direction,

            "score": score,

            "current_price": current_price,

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "risk_distance": risk,

            "reward_distance": reward,

            "rr": round(
                rr,
                2
            ),

            "zone": zone,

            "trigger": "ENTRY_NOW",

            "execution": "MANUAL",

            "invalidation": self._invalidation(
                zone,
                direction
            )
        }

    # ==================================================
    # ZONE SELECTION
    # ==================================================

    def _select_zone(
        self,
        opportunity
    ):

        relevant_zones = opportunity.get(
            "relevant_zones"
        )

        if not isinstance(
            relevant_zones,
            dict
        ):

            return None

        direction = str(
            opportunity.get(
                "direction",
                ""
            )
        ).upper()

        candidates = []

        for key in (
            "fvg",
            "order_blocks"
        ):

            zones = relevant_zones.get(
                key,
                []
            )

            if not isinstance(
                zones,
                list
            ):
                continue

            for zone in zones:

                if not isinstance(
                    zone,
                    dict
                ):
                    continue

                zone_direction = str(
                    zone.get(
                        "direction",
                        direction
                    )
                ).upper()

                if zone_direction != direction:

                    continue

                candidates.append(
                    zone
                )

        if not candidates:

            return None

        # Closest aligned zone first.
        candidates.sort(
            key=lambda item: float(
                item.get(
                    "distance_pct",
                    999
                )
            )
        )

        return candidates[0]

    # ==================================================
    # ENTRY PRICE
    # ==================================================

    def _entry_price(
        self,
        zone
    ):

        for key in (
            "entry",
            "price",
            "midpoint",
            "level"
        ):

            value = zone.get(
                key
            )

            if value is not None:

                try:

                    return float(
                        value
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

        # Use zone midpoint.
        high = zone.get(
            "high"
        )

        low = zone.get(
            "low"
        )

        if (
            high is not None
            and low is not None
        ):

            try:

                return (
                    float(high)
                    + float(low)
                ) / 2

            except (
                TypeError,
                ValueError
            ):

                pass

        return None

    # ==================================================
    # STOP LOSS
    # ==================================================

    def _stop_loss(
        self,
        zone,
        direction
    ):

        # Explicit invalidation.
        invalidation = zone.get(
            "invalidation"
        )

        if invalidation is not None:

            try:

                return float(
                    invalidation
                )

            except (
                TypeError,
                ValueError
            ):

                pass

        low = zone.get(
            "low"
        )

        high = zone.get(
            "high"
        )

        try:

            if direction == "BULLISH":

                if low is not None:

                    return float(
                        low
                    )

            if direction == "BEARISH":

                if high is not None:

                    return float(
                        high
                    )

        except (
            TypeError,
            ValueError
        ):

            pass

        return None

    # ==================================================
    # TAKE PROFIT
    # ==================================================

    def _take_profit(
        self,
        opportunity,
        entry,
        risk,
        direction
    ):

        liquidity = opportunity.get(
            "liquidity"
        )

        if not isinstance(
            liquidity,
            dict
        ):

            return None

        if direction == "BULLISH":

            targets = liquidity.get(
                "buy_side",
                []
            )

        else:

            targets = liquidity.get(
                "sell_side",
                []
            )

        return self._nearest_target(
            targets,
            entry,
            direction
        )

    # ==================================================
    # TARGET SELECTION
    # ==================================================

    def _nearest_target(
        self,
        targets,
        entry,
        direction
    ):

        if not isinstance(
            targets,
            list
        ):

            return None

        candidates = []

        for target in targets:

            if isinstance(
                target,
                dict
            ):

                value = (
                    target.get("price")
                    or target.get("level")
                )

            else:

                value = target

            if value is None:

                continue

            try:

                value = float(
                    value
                )

            except (
                TypeError,
                ValueError
            ):

                continue

            if direction == "BULLISH":

                if value > entry:

                    candidates.append(
                        value
                    )

            elif direction == "BEARISH":

                if value < entry:

                    candidates.append(
                        value
                    )

        if not candidates:

            return None

        if direction == "BULLISH":

            return min(
                candidates
            )

        return max(
            candidates
        )

    # ==================================================
    # TRIGGER STATE
    # ==================================================

    def _get_trigger_state(
        self,
        current_price,
        zone,
        direction
    ):

        low = zone.get(
            "low"
        )

        high = zone.get(
            "high"
        )

        if (
            low is None
            or high is None
        ):

            return "WAITING_FOR_ZONE"

        try:

            low = float(
                low
            )

            high = float(
                high
            )

        except (
            TypeError,
            ValueError
        ):

            return "WAITING_FOR_ZONE"

        # Normalize malformed zones.
        if low > high:

            low, high = high, low

        # ==================================================
        # PRICE INSIDE ZONE
        # ==================================================

        if (
            low
            <= current_price
            <= high
        ):

            return "ENTRY_NOW"

        # ==================================================
        # PRICE ABOVE ZONE
        # ==================================================

        if current_price > high:

            if direction == "BULLISH":

                return "WAITING_FOR_RETRACE"

            return "ZONE_INVALIDATED"

        # ==================================================
        # PRICE BELOW ZONE
        # ==================================================

        if current_price < low:

            if direction == "BEARISH":

                return "WAITING_FOR_RETRACE"

            return "ZONE_INVALIDATED"

        return "WAITING"

    # ==================================================
    # INVALIDATION
    # ==================================================

    def _invalidation(
        self,
        zone,
        direction
    ):

        if direction == "BULLISH":

            return (
                "price closes below "
                "entry-zone invalidation"
            )

        if direction == "BEARISH":

            return (
                "price closes above "
                "entry-zone invalidation"
            )

        return "direction invalidated"