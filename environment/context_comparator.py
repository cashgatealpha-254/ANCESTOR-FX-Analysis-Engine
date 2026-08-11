from datetime import datetime


class ContextComparator:

    def compare(
        self,
        previous_context,
        current_context
    ):

        if previous_context is None:

            return {
                "status": "NO_PREVIOUS_CONTEXT",
                "changes": [],
                "has_changes": False
            }

        changes = []

        self._compare_value(
            changes,
            "direction",
            previous_context,
            current_context
        )

        self._compare_value(
            changes,
            "location",
            previous_context,
            current_context
        )

        self._compare_value(
            changes,
            "confluence",
            previous_context,
            current_context
        )

        self._compare_value(
            changes,
            "market_profile",
            previous_context,
            current_context
        )

        self._compare_zones(
            changes,
            previous_context,
            current_context
        )

        return {

            "status": "OK",

            "has_changes": bool(changes),

            "change_count": len(changes),

            "changes": changes,

            "comparison_time": (
                datetime.utcnow().isoformat()
            )
        }

    # ==================================================
    # VALUE COMPARISON
    # ==================================================

    @staticmethod
    def _compare_value(
        changes,
        field,
        previous,
        current
    ):

        old_value = previous.get(field)
        new_value = current.get(field)

        if old_value != new_value:

            changes.append({

                "type": "VALUE_CHANGED",

                "field": field,

                "previous": old_value,

                "current": new_value
            })

    # ==================================================
    # ZONE COMPARISON
    # ==================================================

    @staticmethod
    def _compare_zones(
        changes,
        previous,
        current
    ):

        old_zones = set(
            str(zone)
            for zone in previous.get(
                "relevant_zones",
                []
            )
        )

        new_zones = set(
            str(zone)
            for zone in current.get(
                "relevant_zones",
                []
            )
        )

        added = new_zones - old_zones
        removed = old_zones - new_zones

        if added:

            changes.append({

                "type": "ZONES_ADDED",

                "zones": list(added)
            })

        if removed:

            changes.append({

                "type": "ZONES_REMOVED",

                "zones": list(removed)
            })