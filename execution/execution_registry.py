import json
import os
from datetime import datetime


class ExecutionRegistry:

    def __init__(
        self,
        file_path="execution/execution_registry.json"
    ):

        self.file_path = file_path

        directory = os.path.dirname(
            self.file_path
        )

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        if not os.path.exists(
            self.file_path
        ):

            self._write([])

    # ==================================================
    # INTERNAL STORAGE
    # ==================================================

    def _read(self):

        try:

            with open(
                self.file_path,
                "r"
            ) as file:

                data = json.load(file)

            if isinstance(
                data,
                list
            ):

                return data

        except (
            OSError,
            json.JSONDecodeError
        ):

            pass

        return []

    def _write(
        self,
        data
    ):

        temporary_file = (
            self.file_path
            + ".tmp"
        )

        with open(
            temporary_file,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        os.replace(
            temporary_file,
            self.file_path
        )

    # ==================================================
    # TRADE ID
    # ==================================================

    @staticmethod
    def build_trade_id(
        setup
    ):

        if not isinstance(
            setup,
            dict
        ):

            return None

        symbol = str(
            setup.get(
                "symbol",
                ""
            )
        ).upper()

        horizon = str(
            setup.get(
                "horizon",
                ""
            )
        ).upper()

        direction = str(
            setup.get(
                "direction",
                ""
            )
        ).upper()

        entry = setup.get(
            "entry"
        )

        stop_loss = setup.get(
            "stop_loss"
        )

        take_profit = setup.get(
            "take_profit"
        )

        signal_id = setup.get(
            "signal_id"
        )

        if not symbol:
            return None

        if not direction:
            return None

        if signal_id:

            return (
                f"{symbol}:"
                f"{horizon}:"
                f"{direction}:"
                f"{signal_id}"
            )

        return (
            f"{symbol}:"
            f"{horizon}:"
            f"{direction}:"
            f"{entry}:"
            f"{stop_loss}:"
            f"{take_profit}"
        )

    # ==================================================
    # LOOKUP
    # ==================================================

    def exists(
        self,
        trade_id
    ):

        if not trade_id:

            return False

        records = self._read()

        return any(
            record.get(
                "trade_id"
            ) == trade_id
            for record in records
            if isinstance(
                record,
                dict
            )
        )

    def get(
        self,
        trade_id
    ):

        if not trade_id:

            return None

        records = self._read()

        for record in records:

            if (
                isinstance(
                    record,
                    dict
                )
                and record.get(
                    "trade_id"
                ) == trade_id
            ):

                return record

        return None

    # ==================================================
    # REGISTER
    # ==================================================

    def register(
        self,
        trade_id,
        status,
        setup=None,
        ticket=None,
        reason=None
    ):

        if not trade_id:

            return {
                "status": "ERROR",
                "reason": "Missing trade ID"
            }

        records = self._read()

        # ----------------------------------------------
        # Duplicate protection
        # ----------------------------------------------

        for record in records:

            if (
                isinstance(
                    record,
                    dict
                )
                and record.get(
                    "trade_id"
                ) == trade_id
            ):

                return {
                    "status": "DUPLICATE",
                    "trade_id": trade_id,
                    "existing_status": record.get(
                        "status"
                    )
                }

        record = {

            "trade_id": trade_id,

            "status": str(
                status
            ).upper(),

            "ticket": ticket,

            "reason": reason,

            "created_at": (
                datetime.utcnow()
                .isoformat()
            ),

            "updated_at": (
                datetime.utcnow()
                .isoformat()
            )
        }

        if isinstance(
            setup,
            dict
        ):

            record["symbol"] = setup.get(
                "symbol"
            )

            record["horizon"] = setup.get(
                "horizon"
            )

            record["direction"] = setup.get(
                "direction"
            )

            record["entry"] = setup.get(
                "entry"
            )

            record["stop_loss"] = setup.get(
                "stop_loss"
            )

            record["take_profit"] = setup.get(
                "take_profit"
            )

        records.append(
            record
        )

        self._write(
            records
        )

        return {
            "status": "REGISTERED",
            "trade_id": trade_id
        }

    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        trade_id,
        status,
        ticket=None,
        reason=None
    ):

        records = self._read()

        for record in records:

            if (
                isinstance(
                    record,
                    dict
                )
                and record.get(
                    "trade_id"
                ) == trade_id
            ):

                record["status"] = str(
                    status
                ).upper()

                record["updated_at"] = (
                    datetime.utcnow()
                    .isoformat()
                )

                if ticket is not None:

                    record["ticket"] = ticket

                if reason is not None:

                    record["reason"] = reason

                self._write(
                    records
                )

                return {
                    "status": "UPDATED",
                    "trade_id": trade_id,
                    "new_status": record[
                        "status"
                    ]
                }

        return {
            "status": "NOT_FOUND",
            "trade_id": trade_id
        }