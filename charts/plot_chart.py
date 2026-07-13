from data.fetcher import get_candles
import MetaTrader5 as mt5

import plotly.graph_objects as go

def create_chart(symbol):
    df = get_candles(symbol, mt5.TIMEFRAME_M15, 200)
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"]
            )
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        title="Ancestor FX",
        xaxis_rangeslider_visible=False
    )

    return fig.to_html(full_html=False)