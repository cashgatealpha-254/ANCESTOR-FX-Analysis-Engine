import json
import os
from datetime import datetime

import MetaTrader5 as mt5


class MT5MarkupPublisher:

    def __init__(
        self,
        filename="horizon_markup.json"
    ):

        self.filename = filename

    # ==================================================
    # PUBLISH
    # ==================================================

    def publish(
        self,
        symbol,
        horizon=None,
        zones=None,
        liquidity=None,
        structure=None,
        trade_setup=None
    ):

        if not symbol:

            return {
                "status": "ERROR",
                "reason": "Missing symbol"
            }

        terminal = mt5.terminal_info()

        if terminal is None:

            return {
                "status": "ERROR",
                "reason": "MT5 terminal unavailable"
            }

        common_path = getattr(
            terminal,
            "commondata_path",
            None
        )

        if not common_path:

            return {
                "status": "ERROR",
                "reason": (
                    "MT5 common data path unavailable"
                )
            }

        files_path = os.path.join(
            common_path,
            "Files"
        )

        os.makedirs(
            files_path,
            exist_ok=True
        )

        payload = {

            "status": "OK",

            "symbol": symbol,

            "horizon": horizon,

            "updated_at": (
                datetime.utcnow()
                .strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
            ),

            "zones": (
                zones
                if isinstance(zones, list)
                else []
            ),

            "liquidity": (
                liquidity
                if isinstance(liquidity, list)
                else []
            ),

            "structure": (
                structure
                if isinstance(structure, list)
                else []
            ),

            "trade_setup": (
                trade_setup
                if isinstance(
                    trade_setup,
                    dict
                )
                else None
            )
        }

        path = os.path.join(
            files_path,
            self.filename
        )

        temp_path = (
            path + ".tmp"
        )

        try:

            with open(
                temp_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    payload,
                    file,
                    indent=2,
                    default=str
                )

            # Atomic replacement where supported.
            os.replace(
                temp_path,
                path
            )

        except Exception as error:

            try:

                if os.path.exists(
                    temp_path
                ):

                    os.remove(
                        temp_path
                    )

            except OSError:

                pass

            return {

                "status": "ERROR",

                "symbol": symbol,

                "reason": (
                    "Unable to publish "
                    "MT5 markup"
                ),

                "error": str(error)
            }

        return {

            "status": "PUBLISHED",

            "symbol": symbol,

            "horizon": horizon,

            "file": path,

            "zones": len(
                payload["zones"]
            ),

            "liquidity": len(
                payload["liquidity"]
            ),

            "structure": len(
                payload["structure"]
            ),

            "has_trade_setup": (
                payload["trade_setup"]
                is not None
            )
        }

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(self):

        terminal = mt5.terminal_info()

        if terminal is None:

            return {
                "status": "ERROR",
                "reason": "MT5 terminal unavailable"
            }

        common_path = getattr(
            terminal,
            "commondata_path",
            None
        )

        if not common_path:

            return {
                "status": "ERROR",
                "reason": (
                    "MT5 common data path unavailable"
                )
            }

        path = os.path.join(
            common_path,
            "Files",
            self.filename
        )

        try:

            if os.path.exists(path):

                os.remove(path)

            return {
                "status": "CLEARED",
                "file": path
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "reason": str(error)
            }