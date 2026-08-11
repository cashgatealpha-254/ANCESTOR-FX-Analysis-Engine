# environment/deep_context_data.py

from data.fetcher import get_candles

from environment.deep_context_config import (
    get_candle_config,
    get_horizon_timeframes,
)


def fetch_timeframe_context(
    symbol,
    timeframe_name
):
    """
    Fetch the configured number of candles
    for one symbol and timeframe.
    """

    config = get_candle_config(
        timeframe_name
    )

    candles = get_candles(
        symbol,
        config["timeframe"],
        config["candles"]
    )

    if candles is None:
        raise ValueError(
            f"No candle data returned for "
            f"{symbol} {timeframe_name}"
        )

    if candles.empty:
        raise ValueError(
            f"Empty candle dataframe for "
            f"{symbol} {timeframe_name}"
        )

    return candles


def fetch_horizon_context(
    symbol,
    horizon
):
    """
    Fetch all configured timeframes
    belonging to a horizon.
    """

    timeframes = get_horizon_timeframes(
        horizon
    )

    context = {}

    for timeframe_name in timeframes:

        context[timeframe_name] = (
            fetch_timeframe_context(
                symbol,
                timeframe_name
            )
        )

    return context


def fetch_full_context(symbol):

    return {

        "SWING": fetch_horizon_context(
            symbol,
            "SWING"
        ),

        "INTRADAY": fetch_horizon_context(
            symbol,
            "INTRADAY"
        ),

        "SCALPING": fetch_horizon_context(
            symbol,
            "SCALPING"
        ),

    }