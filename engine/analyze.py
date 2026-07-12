from analysis import supply_demand
from analysis import liquidity
from analysis import choch
from data.fetcher import connect_mt5, disconnect_mt5
from data.get_candles import get_candles

from indicators import atr
from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi, analyze_rsi
from indicators.atr import calculate_atr, analyze_atr

from analysis.trend import analyze_trend
from analysis.market_state import analyze_market_state
from analysis.market_bias import analyze_market_bias
from analysis.market_structure import analyze_market_structure
from analysis.support_resistance import analyze_support_resistance

from analysis.bos import analyze_bos
from analysis.choch import analyze_choch
from analysis.liquidity import analyze_liquidity
from analysis.supply_demand import analyze_supply_demand

from analysis.swings import detect_swings
from analysis.structure_memory import build_structure_memory
from analysis.protected_levels import detect_protected_levels
from analysis.structure_strength import analyze_structure_strength

from analysis.confluence import analyze_confluence
from analysis.execution import analyze_execution
from analysis.reasoning import ReasoningEngine
from analysis.multi_timeframe import analyze_multi_timeframe
from analysis.market_context import analyze_market_context

from strategy.decision import DecisionEngine
from strategy.execution import ExecutionEngine
from strategy.grade import GradeEngine
from strategy.setup import SetupEngine
from strategy.execution import ExecutionEngine
from strategy.risk import RiskEngine

from engine.confidence import calculate_confidence
from engine.logger import save_analysis

from alerts.notify import send_alert

from mt5.connection import connect_mt5, disconnect_mt5


decision_engine = DecisionEngine()
grade_engine = GradeEngine()
setup_engine = SetupEngine()
execution_engine = ExecutionEngine()
risk_engine = RiskEngine()
reasoning_engine = ReasoningEngine()
save_analysis = save_analysis
send_alert = send_alert


def run_analysis(symbol):

    if not connect_mt5():
         return {"error": "Failed to connect to MT5"}

    print("="*50)
    print("Starting Analysis")
    print("="*50)

    connect_mt5()

    send_alert("🚨 Starting Analysis 🚨")

    try:

        df = get_candles(symbol.upper(), n=100)

        df = calculate_ema(df, 20)
        df = calculate_ema(df, 50)

        df = calculate_rsi(df)
        df = calculate_atr(df)

        trend = analyze_trend(df)
        rsi = analyze_rsi(df)
        atr = analyze_atr(df)

        market_state = analyze_market_state(
            trend,
            rsi,
            atr
        )

        market_bias = analyze_market_bias(
            trend,
            rsi,
            atr,
            market_state
        )

        market_structure = analyze_market_structure(df)

        multi_timeframe = analyze_multi_timeframe(symbol)
 
        levels = analyze_support_resistance(df)

        bos = analyze_bos(df)
        choch = analyze_choch(df)

        liquidity = analyze_liquidity(df)
        supply_demand = analyze_supply_demand(df)
        print(supply_demand)

        market_context = analyze_market_context(
            multi_timeframe,
            market_bias["Market Bias"],
            market_structure["Structure"],
            supply_demand["Current Zone"]
        )

        swings = detect_swings(df)
        structure_memory = build_structure_memory(swings)
        protected_levels = detect_protected_levels(structure_memory)
        structure_strength = analyze_structure_strength(structure_memory)

        confidence = calculate_confidence({
            "trend": trend["Trend"],
            "bos": bos,
            "choch": choch["CHoCH"],
            "liquidity": liquidity,
            "supply_demand": supply_demand["Current Zone"],
            "atr": atr["ATR"]
        })

        send_alert("🚨 Confidence Calculation Complete 🚨")


        results = {
            "trend": trend,
            "bos": bos,
            "choch": choch,
            "liquidity": liquidity,
            "supply_demand": supply_demand,
            "market_structure": market_structure
        }

        confluence = analyze_confluence(results)
        
        print("Reached confidence calculation")
        send_alert("🚨 Confidence Calculation Complete 🚨")
        grade = grade_engine.grade(confidence)
        print(f"Grade: {grade}")
        print(f"Confidence: {confidence}")

        if grade == "NO TRADE":
             send_alert("⚪ No trade setup detected")

        if grade == "C":
             send_alert("🔴 Grade C setup detected")

        if grade == "B":
             send_alert("🟡 Grade B setup detected")

        elif grade == "A":
             send_alert("🟢 Grade A setup detected")

        elif grade == "A+":
             send_alert("🔥 Grade A+ setup detected")

        decision = decision_engine.evaluate({
            "trend": trend["Trend"],
            "confidence": confidence,
            "structure_memory": structure_memory,
            "protected_levels": protected_levels,
            "structure_strength": structure_strength["Structure Strength"],
            "market_bias": market_bias["Market Bias"],
            "market_state": market_state["Market State"],
            "market_structure": market_structure["Structure"]
        })

        setup = setup_engine.build({
            "trend": trend["Trend"],
            "Decision": decision["decision"],
            "support": levels["Support"],
            "resistance": levels["Resistance"],
            "supply_demand": supply_demand["Current Zone"],
            "atr": atr["ATR"],
            "rsi": rsi["RSI"],
        })

        execution = execution_engine.execute(decision, setup, df["close"].iloc[-1])

        current_price = df["close"].iloc[-1]

        execution = analyze_execution(
            symbol,
            trend,
            supply_demand,
            protected_levels,
            atr,
            current_price
        )

        send_alert("🚨 Execution complete🚨")
        print("Execution:", execution)

        risk = risk_engine.calculate(
            execution["entry"],
            execution["sl"],
            execution["tp"]
        )

        reasoning = reasoning_engine.explain({
            "trend": trend["Trend"],
            "market_bias": market_bias["Market Bias"],
            "market_structure": market_structure["Structure"],
            "bos": bos,
            "choch": choch["CHoCH"],
            "liquidity": liquidity,
            "supply_demand": supply_demand["Current Zone"],
        })

        send_alert("🚨 Analysis Complete 🚨")

        return {
            "symbol": symbol.upper(),
            "trend": trend["Trend"],
            "rsi": rsi,
            "atr": atr,
            "market_state": market_state["Market State"],
            "market_bias": market_bias["Market Bias"],
            "market_structure": market_structure["Structure"],
            "support_resistance": levels,
            "bos": bos,
            "choch": choch,
            "liquidity": liquidity,
            "supply_demand": supply_demand,
            "swings": swings,
            "structure_memory": structure_memory,
            "protected_levels": protected_levels,
            "structure_strength": structure_strength["Structure Strength"],
            "confidence": confidence,
            "confluence": confluence,
            "grade": grade,
            "decision": decision,
            "setup": setup,
            "execution": execution,
            "risk": risk,
            "reasoning": reasoning,
            "multi_timeframe": multi_timeframe,
            "market_context": market_context,
            "execution" : execution
        }

    finally:
        disconnect_mt5()