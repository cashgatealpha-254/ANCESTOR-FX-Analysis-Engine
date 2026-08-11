from data.fetcher import get_candles
import MetaTrader5 as mt5
import plotly.graph_objects as go


def create_chart(symbol):

    try:
        df = get_candles(
            symbol,
            mt5.TIMEFRAME_M15,
            200
        )

        # No market data available
        if df is None or df.empty:
            return f"""
            <div style="
                padding:20px;
                background:#1e293b;
                border-radius:12px;
                color:#f59e0b;
                text-align:center;
            ">
                <h3>Chart Unavailable</h3>
                <p>No M15 market data available for {symbol}.</p>
                <p>The analysis engine can continue without the chart.</p>
            </div>
            """

        # Build candlestick chart
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
            title=f"Ancestor FX — {symbol} M15",
            xaxis_rangeslider_visible=False,
            height=600,
            margin=dict(
                l=40,
                r=40,
                t=60,
                b=40
            )
        )

        return fig.to_html(
            full_html=False,
            include_plotlyjs="cdn"
        )

    except Exception as e:

        print(f"Chart error for {symbol}: {e}")

        return f"""
        <div style="
            padding:20px;
            background:#1e293b;
            border-radius:12px;
            color:#ef4444;
            text-align:center;
        ">
            <h3>Chart Error</h3>
            <p>Unable to load the {symbol} chart.</p>
            <small>{str(e)}</small>
        </div>
        """