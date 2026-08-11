import json
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

from environment.context_schema import ContextSchema
from environment.context_validator import ContextValidator


class DeepContextStore:

    def __init__(self, base_dir="data/deep_context"):

        self.base_dir = Path(base_dir)

        self.base_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.validator = ContextValidator()

    # ==================================================
    # SAVE CONTEXT
    # ==================================================

    def save(
        self,
        symbol,
        horizon,
        context
    ):

        # ==============================================
        # NORMALIZE CONTEXT
        # ==============================================

        normalized_context = ContextSchema.build(
            symbol=symbol,
            horizon=horizon,
            context=context
        )

        # ==============================================
        # VALIDATE CONTEXT
        # ==============================================

        validation = self.validator.validate(
            normalized_context
        )

        if not validation["valid"]:

            return {

                "status": "REJECTED",

                "symbol": symbol,

                "horizon": horizon,

                "errors": validation["errors"]
            }

        # ==============================================
        # CREATE SNAPSHOT
        # ==============================================

        timestamp = datetime.utcnow()

        snapshot = {

            "context_version": (
                timestamp.strftime(
                    "%Y%m%d_%H%M%S"
                )
            ),

            "analysis_time": (
                timestamp.isoformat()
            ),

            "symbol": symbol,

            "horizon": horizon,

            "context": normalized_context
        }

        # ==============================================
        # FILE PATH
        # ==============================================

        file_path = self.base_dir / (

            f"{symbol}_{horizon}.json"

        )

        # ==============================================
        # WRITE
        # ==============================================

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                snapshot,
                file,
                indent=4,
                default=self._serialize
            )

        return snapshot

    # ==================================================
    # LOAD LATEST CONTEXT
    # ==================================================

    def load(
        self,
        symbol,
        horizon
    ):

        file_path = self.base_dir / (

            f"{symbol}_{horizon}.json"

        )

        if not file_path.exists():

            return None

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except (
            json.JSONDecodeError,
            OSError
        ):

            return None

    # ==================================================
    # CHECK WHETHER CONTEXT EXISTS
    # ==================================================

    def exists(
        self,
        symbol,
        horizon
    ):

        file_path = self.base_dir / (

            f"{symbol}_{horizon}.json"

        )

        return file_path.exists()

    # ==================================================
    # SERIALIZATION
    # ==================================================

    @staticmethod
    def _serialize(value):

        if isinstance(
            value,
            (
                pd.Timestamp,
                datetime
            )
        ):

            return value.isoformat()

        if isinstance(
            value,
            np.generic
        ):

            return value.item()

        if isinstance(
            value,
            np.ndarray
        ):

            return value.tolist()

        if isinstance(
            value,
            set
        ):

            return list(value)

        return str(value)