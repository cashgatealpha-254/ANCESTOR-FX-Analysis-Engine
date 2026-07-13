from data.get_candles import get_candles


import MetaTrader5 as mt5
import pandas as pd


from analysis.trend import analyze_trend
from analysis.recent_structure import analyze_recent_structure

from indicators.ema import calculate_ema


def analyze_multi_timeframe(symbol):

    h4 = get_candles(symbol, timeframe="H4", n=150)
    h4 = calculate_ema(h4, 20)
    h4 = calculate_ema(h4, 50)

    h1 = get_candles(symbol, timeframe="H1", n=150)
    h1 = calculate_ema(h1, 20)
    h1= calculate_ema(h1, 50)

    m15 = get_candles(symbol, timeframe="M15", n=150)
    m15 = calculate_ema(m15, 20)
    m15 = calculate_ema(m15, 50)

    h4_trend = analyze_trend(h4)
    h1_structure = analyze_recent_structure(h1)
    m15_structure = analyze_recent_structure(m15)

    alignment = (
        h4_trend["Trend"] ==
        h1_structure["Structure"]
    )

    return {
        "H4 Trend": h4_trend["Trend"],
        "H1 Structure": h1_structure["Structure"],
        "M15 Structure": m15_structure["Structure"],
        "alignment": alignment
    }