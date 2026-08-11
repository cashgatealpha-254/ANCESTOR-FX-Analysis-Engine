import MetaTrader5 as mt5
import pandas as pd

from mt5.connection import connect_mt5


def ensure_connection():
    """
    Ensure that the shared MT5 connection is active.
    """

    if not connect_mt5():
        raise Exception(
            f"MT5 connection failed: {mt5.last_error()}"
        )


def ensure_symbol(symbol: str):
    """
    Make sure the requested symbol exists and is visible
    in MT5 Market Watch.
    """

    ensure_connection()

    info = mt5.symbol_info(symbol)

    if info is None:
        raise Exception(
            f"Symbol {symbol} not found in MT5. "
            f"MT5 error: {mt5.last_error()}"
        )

    if not info.visible:
        if not mt5.symbol_select(symbol, True):
            raise Exception(
                f"Failed to select {symbol} in MT5 Market Watch. "
                f"MT5 error: {mt5.last_error()}"
            )

    return info


def get_price(symbol: str):
    """
    Get current bid/ask price from MT5.
    """

    ensure_symbol(symbol)

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        raise Exception(
            f"Failed to get price for {symbol}. "
            f"MT5 error: {mt5.last_error()}"
        )

    return {
        "symbol": symbol,
        "bid": tick.bid,
        "ask": tick.ask,
        "spread": tick.ask - tick.bid,
        "time": tick.time
    }


def get_candles(symbol, timeframe, bars):
    """
    Retrieve OHLCV candles from MetaTrader 5.
    """

    ensure_symbol(symbol)

    rates = mt5.copy_rates_from_pos(
        symbol,
        timeframe,
        0,
        bars
    )

    if rates is None:
        raise Exception(
            f"Failed to get candles for {symbol}. "
            f"Timeframe: {timeframe}, "
            f"Bars: {bars}, "
            f"MT5 error: {mt5.last_error()}"
        )

    if len(rates) == 0:
        raise Exception(
            f"No candles returned for {symbol}. "
            f"Timeframe: {timeframe}, "
            f"Bars: {bars}"
        )

    df = pd.DataFrame(rates)

    if df.empty:
        raise Exception(
            f"Empty candle dataframe for {symbol}"
        )

    df["time"] = pd.to_datetime(
        df["time"],
        unit="s"
    )

    df.set_index(
        "time",
        inplace=True
    )

    return df