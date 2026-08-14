from pathlib import Path
from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd


class CandleCache:

    DEEP_CONTEXT_BARS = {
        "D1": 90,
        "H4": 540,
        "H1": 2160,
        "M15": 3840,
        "M5": 4320,
    }

    TIMEFRAME_MAPPING = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
        "W1": mt5.TIMEFRAME_W1,
        "MN1": mt5.TIMEFRAME_MN1,
    }

    def __init__(
        self,
        base_dir="data/deep_context/candles"
    ):

        self.base_dir = Path(base_dir)

        self.base_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ======================================================
    # PATH
    # ======================================================

    def _path(
        self,
        symbol,
        timeframe
    ):

        symbol_dir = (
            self.base_dir / symbol
        )

        symbol_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        return (
            symbol_dir /
            f"{timeframe}.parquet"
        )

    # ======================================================
    # GET TIMEFRAME
    # ======================================================

    def _get_timeframe(
        self,
        timeframe
    ):

        if isinstance(
            timeframe,
            str
        ):

            timeframe = (
                timeframe.upper()
            )

            if timeframe not in self.TIMEFRAME_MAPPING:

                raise ValueError(
                    f"Unsupported timeframe: {timeframe}"
                )

            return self.TIMEFRAME_MAPPING[
                timeframe
            ]

        return timeframe

    # ======================================================
    # FETCH INITIAL DATA
    # ======================================================

    def _fetch_initial(
        self,
        symbol,
        timeframe,
        bars
    ):

        mt5_timeframe = (
            self._get_timeframe(
                timeframe
            )
        )

        rates = mt5.copy_rates_from_pos(
            symbol,
            mt5_timeframe,
            0,
            bars
        )

        if rates is None:

            raise Exception(
                f"Failed to fetch {timeframe} "
                f"candles for {symbol}. "
                f"MT5 error: {mt5.last_error()}"
            )

        if len(rates) == 0:

            raise Exception(
                f"No {timeframe} candles "
                f"available for {symbol}"
            )

        df = pd.DataFrame(
            rates
        )

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )

        columns = [
            "time",
            "open",
            "high",
            "low",
            "close",
            "tick_volume"
        ]

        df = df[
            [
                c for c in columns
                if c in df.columns
            ]
        ]

        df = (
            df
            .drop_duplicates(
                subset=["time"]
            )
            .sort_values("time")
            .reset_index(drop=True)
        )

        return df

    # ======================================================
    # LOAD CACHE
    # ======================================================

    def load(
        self,
        symbol,
        timeframe
    ):

        path = self._path(
            symbol,
            timeframe
        )

        if not path.exists():

            return None

        try:

            df = pd.read_parquet(
                path
            )

            if "time" in df.columns:

                df["time"] = pd.to_datetime(
                    df["time"]
                )

            df = (
                df
                .drop_duplicates(
                    subset=["time"]
                )
                .sort_values("time")
                .reset_index(drop=True)
            )

            return df

        except Exception as exc:

            print(
                f"Cache load failed for "
                f"{symbol} {timeframe}: {exc}"
            )

            return None

    # ======================================================
    # SAVE CACHE
    # ======================================================

    def save(
        self,
        symbol,
        timeframe,
        df
    ):

        if df is None or df.empty:

            raise ValueError(
                "Cannot save empty candle data."
            )

        path = self._path(
            symbol,
            timeframe
        )

        temp_path = path.with_suffix(
            ".tmp.parquet"
        )

        df = (
            df
            .copy()
            .drop_duplicates(
                subset=["time"]
            )
            .sort_values("time")
            .reset_index(drop=True)
        )

        df.to_parquet(
            temp_path,
            index=False
        )

        temp_path.replace(
            path
        )

        return df

    # ======================================================
    # BUILD / UPDATE CACHE
    # ======================================================

    def get(
        self,
        symbol,
        timeframe,
        bars=None
    ):

        timeframe = timeframe.upper()

        if bars is None:

            bars = self.DEEP_CONTEXT_BARS.get(
                timeframe
            )

        if bars is None:

            raise ValueError(
                f"No bar allocation configured "
                f"for {timeframe}"
            )

        cached = self.load(
            symbol,
            timeframe
        )

        # --------------------------------------------------
        # FIRST DOWNLOAD
        # --------------------------------------------------

        if cached is None:

            print(
                f"Downloading {symbol} "
                f"{timeframe}: {bars} candles"
            )

            df = self._fetch_initial(
                symbol,
                timeframe,
                bars
            )

            self.save(
                symbol,
                timeframe,
                df
            )

            return df

        # --------------------------------------------------
        # CACHE EXISTS
        # --------------------------------------------------

        if cached.empty:

            df = self._fetch_initial(
                symbol,
                timeframe,
                bars
            )

            self.save(
                symbol,
                timeframe,
                df
            )

            return df

        latest_time = cached[
            "time"
        ].max()

        mt5_timeframe = (
            self._get_timeframe(
                timeframe
            )
        )

        # --------------------------------------------------
        # FETCH NEWEST WINDOW
        #
        # We deliberately request a small overlap so
        # partially formed/current candles are refreshed.
        # --------------------------------------------------

        refresh_bars = 10

        rates = mt5.copy_rates_from_pos(
            symbol,
            mt5_timeframe,
            0,
            refresh_bars
        )

        if rates is None:

            print(
                f"Could not refresh "
                f"{symbol} {timeframe}; "
                f"using cached data."
            )

            return cached

        if len(rates) == 0:

            return cached

        fresh = pd.DataFrame(
            rates
        )

        fresh["time"] = pd.to_datetime(
            fresh["time"],
            unit="s"
        )

        columns = [
            "time",
            "open",
            "high",
            "low",
            "close",
            "tick_volume"
        ]

        fresh = fresh[
            [
                c for c in columns
                if c in fresh.columns
            ]
        ]

        # --------------------------------------------------
        # MERGE
        # --------------------------------------------------

        combined = pd.concat(
            [
                cached,
                fresh
            ],
            ignore_index=True
        )

        combined = (
            combined
            .drop_duplicates(
                subset=["time"],
                keep="last"
            )
            .sort_values("time")
            .reset_index(drop=True)
        )

        # --------------------------------------------------
        # MAINTAIN ALLOCATION
        # --------------------------------------------------

        if len(combined) > bars:

            combined = combined.tail(
                bars
            ).reset_index(
                drop=True
            )

        self.save(
            symbol,
            timeframe,
            combined
        )

        return combined

    # ======================================================
    # GET FULL DEEP CONTEXT
    # ======================================================

    def build_symbol_context(
        self,
        symbol
    ):

        context = {}

        for timeframe in self.DEEP_CONTEXT_BARS:

            print(
                f"\nLoading "
                f"{symbol} {timeframe}"
            )

            context[timeframe] = self.get(
                symbol,
                timeframe
            )

        return context

    # ======================================================
    # CACHE STATUS
    # ======================================================

    def status(
        self,
        symbol
    ):

        result = {}

        for timeframe, bars in (
            self.DEEP_CONTEXT_BARS.items()
        ):

            df = self.load(
                symbol,
                timeframe
            )

            if df is None or df.empty:

                result[timeframe] = {
                    "status": "MISSING",
                    "bars": 0,
                    "expected": bars,
                    "latest": None,
                    "oldest": None
                }

                continue

            result[timeframe] = {

                "status": "READY",

                "bars": len(df),

                "expected": bars,

                "latest": (
                    df["time"]
                    .max()
                    .isoformat()
                ),

                "oldest": (
                    df["time"]
                    .min()
                    .isoformat()
                )
            }

        return result