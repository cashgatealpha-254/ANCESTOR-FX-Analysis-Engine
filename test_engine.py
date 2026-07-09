from data.fetcher import connect_mt5, disconnect_mt5
from data.get_candles import get_candles

from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi, analyze_rsi
from indicators.atr import calculate_atr, analyze_atr

from analysis.trend import analyze_trend
from analysis.market_state import analyze_market_state
from analysis.market_bias import analyze_market_bias
from analysis.support_resistance import analyze_support_resistance
from analysis.market_structure import analyze_market_structure
from analysis.confidence import calculate_confidence
from analysis.signal import generate_signal


def main():

    connect_mt5()

    try:

        # Fetch market data
        df = get_candles("GBPUSD", n=100)

        # Calculate Indicators
        df = calculate_ema(df, period=20)
        df = calculate_ema(df, period=50)

        df = calculate_rsi(df)

        df = calculate_atr(df)

        # Analyze Indicators
        trend = analyze_trend(df)
        rsi = analyze_rsi(df)
        atr = analyze_atr(df)

        # Market State
        market_state = analyze_market_state(
            trend,
            rsi,
            atr
        )

        # Market Bias
        market_bias = analyze_market_bias(
            trend,
            rsi,
            atr,
            market_state
        )
        structure = analyze_market_structure(df)
        levels = analyze_support_resistance(df)
        bos = structure.get("bos")
        choch = structure.get("choch")
        liquidity = structure.get("liquidity")
        supply_demand = structure.get("supply_demand")
        structure_memory = structure.get("structure_memory")
        protected_levels = structure.get("protected_levels")
        structure_strength = structure.get("structure_strength")

        confidence = calculate_confidence(
            trend,
            rsi,
            atr,
            market_state,
            market_bias,
            structure,
            bos,
            choch,
            liquidity,
            supply_demand,
            structure_memory,
            protected_levels,
            structure_strength
        )
        signal = generate_signal(
            trend,
            market_bias,
            confidence
        )

        # Output
        print("\n========== MARKET ANALYSIS ENGINE ==========")

        print("\nTrend")
        print(trend)

        print("\nRSI")
        print(rsi)

        print("\nATR")
        print(atr)

        print("\nMarket State")
        print(market_state)

        print("\nMarket Bias")
        print(market_bias)

        print("\nSupport and Resistance Levels")
        print(levels)

        print("\nMarket Structure")
        print(structure)

        print("\nConfidence")
        print(confidence)

        print("\nTrading Signal")
        print(signal)

    finally:

        disconnect_mt5()


if __name__ == "__main__":
    main()