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
from analysis.recent_structure import analyze_recent_structure
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
from analysis.validation import validate_analysis

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

    send_alert("🚀 Starting Analysis")

    # -------------------------
    # CONNECT
    # -------------------------
    if not connect_mt5():
        send_alert("❌ MT5 Connection Failed")
        return {"error": "Failed to connect to MT5"}

    try:

        send_alert(f"📈 Fetching candles for {symbol}")

        # -------------------------
        # DATA
        # -------------------------
        df = get_candles(symbol.upper(), n=100)

        # -------------------------
        # INDICATORS
        # -------------------------
        send_alert("📊 Calculating Indicators")

        df = calculate_ema(df, 20)
        df = calculate_ema(df, 50)
        df = calculate_rsi(df)
        df = calculate_atr(df)

        # -------------------------
        # ANALYSIS
        # -------------------------
        send_alert("🧠 Running Market Analysis")

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

        swings = detect_swings(df)
        structure_memory = build_structure_memory(swings)
        protected_levels = detect_protected_levels(structure_memory)

        bos = analyze_bos(df, swings)
        choch = analyze_choch(df, protected_levels)

        supply_demand = analyze_supply_demand(df, swings)
        liquidity = analyze_liquidity(df, swings)

        levels = analyze_support_resistance(df)

        structure_strength = analyze_structure_strength(structure_memory)

        market_structure = analyze_recent_structure(df)

        supply_demand = analyze_supply_demand(df, swings)

      # Get the zone safely
        current_zone = supply_demand.get("Current Zone")

        if current_zone is None:
         current_zone = supply_demand.get("current_zone")

        elif current_zone is None:
          current_zone = "UNKNOWN"

       
       
        multi_timeframe = analyze_multi_timeframe(symbol)

        market_context = analyze_market_context(
         multi_timeframe,
         market_bias["Market Bias"],
         market_structure["Structure"],
         current_zone
       )

        # -------------------------
        # CONFIDENCE
        # -------------------------
        send_alert("📊 Calculating Confidence")

        confidence = calculate_confidence({
         "trend": trend["Trend"],
         "bos": bos["BOS"],
         "choch": choch["CHoCH"],
         "liquidity": liquidity["Liquidity"],
         "supply_demand": supply_demand["Current Zone"],
         "atr": atr["Volatility"]
        })

        results = {
    "trend": trend,
    "bos": bos,
    "choch": choch,
    "liquidity": liquidity,
    "supply_demand": supply_demand,
    "market_structure": market_structure,
    "structure_memory": structure_memory,
    "protected_levels": protected_levels
}

        
        confluence = analyze_confluence(results)

        grade = grade_engine.grade(confidence)

        send_alert(f"🎯 Grade: {grade}")

        # -------------------------
        # STRATEGY
        # -------------------------
        send_alert("⚙️ Building Strategy")

        decision = decision_engine.evaluate({
    "trend": trend["Trend"],
    "confidence": confidence,
    "market_bias": market_bias["Market Bias"],
    "market_state": market_state["Market State"],
    "market_structure": market_structure["Structure"],
    "structure_memory": structure_memory,
    "protected_levels": protected_levels,
    "structure_strength": structure_strength["Structure Strength"]
})

        setup = setup_engine.build({
    "decision": decision["decision"],
    "support": levels["Support"],
    "resistance": levels["Resistance"]
})

        execution = execution_engine.execute(
            decision,
            setup,
            df["close"].iloc[-1]
        )

        # -------------------------
        # RISK
        # -------------------------
        send_alert("🛡️ Calculating Risk")

        risk = None

        if execution["entry"] is not None:
            risk = risk_engine.calculate(
                execution["entry"],
                execution["stop_loss"],
                execution["take_profit"]
            )

        # -------------------------
        # REASONING
        # -------------------------
        send_alert("🧾 Generating Reasoning")

        reasoning = reasoning_engine.explain({
    "trend": trend["Trend"],
    "market_bias": market_bias["Market Bias"],
    "market_structure": market_structure["Structure"],
    "bos": bos,
    "choch": choch["CHoCH"],
    "liquidity": liquidity,
    "supply_demand": supply_demand["Current Zone"]
})
        send_alert("✅ Analysis Complete")

        return {
    "symbol": symbol.upper(),
    "trend": trend,
    "market_bias": market_bias,
    "market state": market_state,
    "market_structure": market_structure,
    "structure_memory" : structure_memory,
    "supply_demand": supply_demand,
    "liquidity": liquidity,
    "protected_levels": protected_levels,
    "bos": bos,
    "choch": choch,
    "confidence": confidence,
    "decision": decision,
    "setup": setup,
    "execution": execution,
    "risk": risk,
    "reasoning": reasoning,
    "grade": grade,
    "confluence": confluence
 }
    

        validation = validate_analysis(results)
        results["validation"] = validation

    finally:
     disconnect_mt5()
send_alert("🔌 MT5 Disconnected")