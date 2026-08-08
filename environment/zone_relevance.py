from typing import Any, Dict, List, Optional


class ZoneRelevance:

    def __init__(self, max_zones: int = 3):

        self.max_zones = max_zones

    # ==================================================
    # PUBLIC API
    # ==================================================

    def analyze(
        self,
        direction: str,
        fvg: Optional[Dict[str, Any]] = None,
        order_blocks: Optional[Dict[str, Any]] = None,
        profile: Optional[Dict[str, Any]] = None,
    ):

        direction = str(
            direction or "NEUTRAL"
        ).upper()

        return {
            "direction": direction,

            "fvg": self._select_directional_zones(
                fvg,
                direction
            ),

            "order_blocks": self._select_directional_zones(
                order_blocks,
                direction
            ),

            "profile": self._select_profile_zones(
                profile,
                direction
            )
        }

    # ==================================================
    # DIRECTIONAL ZONES
    # ==================================================

    def _select_directional_zones(
        self,
        zones,
        direction
    ):

        if not isinstance(
            zones,
            dict
        ):

            return []

        if direction == "BULLISH":

            candidates = zones.get(
                "bullish",
                []
            )

        elif direction == "BEARISH":

            candidates = zones.get(
                "bearish",
                []
            )

        else:

            candidates = (
                zones.get("bullish", [])
                + zones.get("bearish", [])
            )

        if not isinstance(
            candidates,
            list
        ):

            return []

        candidates = [
            zone
            for zone in candidates
            if isinstance(
                zone,
                dict
            )
        ]

        # ----------------------------------------------
        # Sort nearest first
        # ----------------------------------------------

        candidates.sort(
            key=self._distance
        )

        return candidates[
            :self.max_zones
        ]

    # ==================================================
    # PROFILE ZONES
    # ==================================================

    def _select_profile_zones(
        self,
        profile,
        direction
    ):

        if not isinstance(
            profile,
            dict
        ):

            return []

        candidates = []

        for zone_type in (
            "POC",
            "VAH",
            "VAL"
        ):

            zone = profile.get(
                zone_type
            )

            if isinstance(
                zone,
                dict
            ):

                candidate = dict(
                    zone
                )

                candidate["type"] = (
                    candidate.get(
                        "type",
                        f"PROFILE_{zone_type}"
                    )
                )

                candidates.append(
                    candidate
                )

            elif isinstance(
                zone,
                (int, float)
            ):

                candidates.append({
                    "type": f"PROFILE_{zone_type}",
                    "price": zone
                })

        candidates.sort(
            key=self._distance
        )

        return candidates[
            :self.max_zones
        ]

    # ==================================================
    # DISTANCE
    # ==================================================

    @staticmethod
    def _distance(
        zone
    ):

        if not isinstance(
            zone,
            dict
        ):

            return float(
                "inf"
            )

        distance = zone.get(
            "distance_pct"
        )

        try:

            return float(
                distance
            )

        except (
            TypeError,
            ValueError
        ):

            return float(
                "inf"
            )