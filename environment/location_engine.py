import pandas as pd


class LocationEngine:

    def __init__(self, proximity_threshold=0.01):
        """
        proximity_threshold:
            Maximum relative distance from current price
            for a level/zone to be considered nearby.

            0.01 = 1%
        """
        self.proximity_threshold = proximity_threshold

    def analyze(
        self,
        df: pd.DataFrame,
        supply_demand=None,
        market_profile=None,
        fvg=None,
        order_blocks=None
    ):
        """
        Determine which important market areas are
        currently close to price.
        """

        if df.empty:
            return {
                "current_price": None,
                "nearby_zones": [],
                "score": 0
            }

        required_columns = {
            "close"
        }

        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        current_price = float(
            df.iloc[-1]["close"]
        )

        zones = []

        # --------------------------------
        # Supply / Demand
        # --------------------------------

        zones.extend(
            self._extract_zones(
                supply_demand,
                current_price
            )
        )

        # --------------------------------
        # FVG
        # --------------------------------

        zones.extend(
            self._extract_fvg(
                fvg,
                current_price
            )
        )

        # --------------------------------
        # Order Blocks
        # --------------------------------

        zones.extend(
            self._extract_order_blocks(
                order_blocks,
                current_price
            )
        )

        # --------------------------------
        # Market Profile
        # --------------------------------

        zones.extend(
            self._extract_profile_levels(
                market_profile,
                current_price
            )
        )

        nearby_zones = [
            zone
            for zone in zones
            if zone["distance_pct"]
            <= self.proximity_threshold * 100
        ]

        score = self._calculate_score(
            nearby_zones
        )

        return {
            "current_price": current_price,
            "nearby_zones": nearby_zones,
            "score": score
        }

    def _extract_zones(
        self,
        supply_demand,
        current_price
    ):

        zones = []

        if not isinstance(
            supply_demand,
            dict
        ):
            return zones

        # Supports common zone formats.
        possible_zones = (
            supply_demand.get("zones", [])
        )

        for zone in possible_zones:

            low = zone.get("low")
            high = zone.get("high")

            if low is None or high is None:
                continue

            zones.append(
                self._build_zone(
                    "SUPPLY_DEMAND",
                    low,
                    high,
                    current_price,
                    zone.get("type")
                )
            )

        return zones

    def _extract_fvg(
        self,
        fvg,
        current_price
    ):

        zones = []

        if not isinstance(fvg, dict):
            return zones

        for direction in [
            "bullish",
            "bearish"
        ]:

            for gap in fvg.get(
                direction,
                []
            ):

                low = gap.get("low")
                high = gap.get("high")

                if low is None or high is None:
                    continue

                zones.append(
                    self._build_zone(
                        "FVG",
                        low,
                        high,
                        current_price,
                        direction.upper()
                    )
                )

        return zones

    def _extract_order_blocks(
        self,
        order_blocks,
        current_price
    ):

        zones = []

        if not isinstance(
            order_blocks,
            dict
        ):
            return zones

        for direction in [
            "bullish",
            "bearish"
        ]:

            for block in order_blocks.get(
                direction,
                []
            ):

                low = block.get("low")
                high = block.get("high")

                if low is None or high is None:
                    continue

                zones.append(
                    self._build_zone(
                        "ORDER_BLOCK",
                        low,
                        high,
                        current_price,
                        direction.upper()
                    )
                )

        return zones

    def _extract_profile_levels(
        self,
        market_profile,
        current_price
    ):

        zones = []

        if not isinstance(
            market_profile,
            dict
        ):
            return zones

        for level_name in [
            "poc",
            "vah",
            "val"
        ]:

            price = market_profile.get(
                level_name
            )

            if price is None:
                continue

            zones.append(
                self._build_level(
                    f"PROFILE_{level_name.upper()}",
                    price,
                    current_price
                )
            )

        return zones

    def _build_zone(
        self,
        zone_type,
        low,
        high,
        current_price,
        direction
    ):

        low = float(low)
        high = float(high)

        midpoint = (
            low + high
        ) / 2

        distance_pct = (
            abs(midpoint - current_price)
            / current_price
        ) * 100

        return {
            "type": zone_type,
            "direction": direction,
            "low": low,
            "high": high,
            "midpoint": midpoint,
            "distance_pct": round(
                distance_pct,
                4
            ),
            "price_inside": (
                low <= current_price <= high
            )
        }

    def _build_level(
        self,
        level_type,
        price,
        current_price
    ):

        price = float(price)

        distance_pct = (
            abs(price - current_price)
            / current_price
        ) * 100

        return {
            "type": level_type,
            "direction": None,
            "price": price,
            "distance_pct": round(
                distance_pct,
                4
            ),
            "price_inside": (
                price == current_price
            )
        }

    @staticmethod
    def _calculate_score(
        nearby_zones
    ):

        if not nearby_zones:
            return 0

        score = 0

        for zone in nearby_zones:

            if zone["type"] == "SUPPLY_DEMAND":
                score += 4

            elif zone["type"] == "FVG":
                score += 3

            elif zone["type"] == "ORDER_BLOCK":
                score += 4

            elif zone["type"].startswith(
                "PROFILE_"
            ):
                score += 2

            if zone.get(
                "price_inside",
                False
            ):
                score += 2

        return min(
            score,
            20
        )