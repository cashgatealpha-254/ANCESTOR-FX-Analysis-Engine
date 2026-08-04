from analysis import supply_demand
from analysis import liquidity
from analysis import choch
from brain.coach import CoachEngine
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
from analysis.narrative import build_narrative
from analysis.checklist import build_checklist
from analysis.execution_quality import analyze_execution_quality
from analysis.wait_signal import analyze_wait_signal
from analysis.final_filter import final_filter
from analysis.fresh_zone import analyze_fresh_zone
from analysis.session_filter import analyze_session
from analysis.trade_score import calculate_trade_score

from analysis.market_memory import update_market_memory
from analysis.continuation import analyze_continuation
from analysis.stability import analyze_stability

from analysis.setup_tracker import track_setup
from analysis.reflection import reflect
from analysis.improvement import analyze_improvements
from analysis.strengths import analyze_strengths
from analysis.watchlist import analyze_watchlist
from analysis.coach import coach

from strategy.decision import DecisionEngine
from strategy.execution import ExecutionEngine
from strategy.grade import GradeEngine
from strategy.setup import SetupEngine
from strategy.risk import RiskEngine
from strategy.execution_plan import ExecutionPlanner

from brain.confidence import calculate
from brain.decision import decide
from brain.advisor import explain
from brain.risk_manager import check
from brain.execution import execution_plan
from brain.memory import MarketMemory
from brain.adaptive_confidence import AdaptiveConfidence
from brain.replay import ReplayEngine
from brain.patterns import PatternEngine
from brain.behavior import BehaviorEngine
from brain.dna import TraderDNA
from brain.evolution import StrategyEvolution 
from brain.replay_studio import ReplayStudio
from brain.intelligence import IntelligenceCore

from engine.confidence import calculate_confidence
from engine.logger import save_analysis
from engine.report import build as build_report
from engine.verdict import build as build_verdict
from engine.summary import build as build_summary
from engine.history import add as add_history
from engine.history import previous
from engine.change_detector import compare
from engine.session_memory import update as update_session
from engine.session_memory import get as session
from engine.health_check import run as health_check
from engine.performance import success, failure, stats

from journal.logger import Journal 

from dashboard.history import save_analysis

from alerts.notify import send_alert

from mt5.connection import connect_mt5, disconnect_mt5


decision_engine = DecisionEngine()
grade_engine = GradeEngine()
setup_engine = SetupEngine()
execution_engine = ExecutionEngine()
risk_engine = RiskEngine()
reasoning_engine = ReasoningEngine()
execution_planner = ExecutionPlanner()
journal = Journal()
memory = MarketMemory()
adaptive_engine = AdaptiveConfidence()
replay_engine = ReplayEngine()
pattern_engine = PatternEngine()
behavior_engine = BehaviorEngine()
dna_engine = TraderDNA()
evolution_engine = StrategyEvolution()
replay_studio = ReplayStudio()
intelligence = IntelligenceCore()
save_analysis = save_analysis
send_alert = send_alert

health = health_check()

results = {
    "health": health
}

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

        structure_strength = analyze_structure_strength(structure_memory)

        market_structure = analyze_recent_structure(df)

      # Get the zone safely
        current_zone = (
            supply_demand.get("Current Zone")
            or
            supply_demand.get("current_zone")
            or "UNKNOWN"
       )
               
        multi_timeframe = analyze_multi_timeframe(symbol)

        levels = analyze_support_resistance(df)
        
        market_context = analyze_market_context(
         multi_timeframe,
         market_bias["Market Bias"],
         market_structure["Structure"],
         current_zone
       )
        
        # -------------------------
        # BUILD RESULTS DICTIONARY
        # -------------------------
        send_alert("Building Dictionary:)")

        results = {
           "symbol": symbol,

            "trend": trend,
            "rsi": rsi,
            "atr": atr,
            "market_bias": market_bias,
            "market_state": market_state,
            "swings": swings,
            "structure_memory": structure_memory,
            "protected_levels": protected_levels,
            "bos": bos,
            "choch": choch,
            "supply_demand": supply_demand,
            "liquidity": liquidity,
            "levels": levels,
            "market_structure": market_structure,
            "structure_strength": structure_strength,
            "multi_timeframe": multi_timeframe,
            "market_context": market_context
       }
        
       
        results["support"] = levels["Support"]
        results["resistance"] = levels["Resistance"]

        # -------------------------
        # CONFIDENCE
        # -------------------------
        send_alert("📊 Calculating Confidence")

        results["confidence"] = calculate_confidence(results)

        # --------------------------
        # CONFLUENCE
        # --------------------------
        send_alert("Getting Confluence")

        results["confluence"] = analyze_confluence(results)

        # --------------------------
        # GRADE
        # --------------------------

        results["grade"] = grade_engine.grade(results["confidence"])

        send_alert(f"🎯 Grade: {results['grade']}")

        # -------------------------
        # DECISION
        # -------------------------
        send_alert("⚙️ Building Decision")

        results["decision"] = decision_engine.evaluate(results)

        # -------------------------
        # REASONS
        # -------------------------

        results["reasons"] = [
            f"Trend: {results['trend']}",
            f"Market Bias: {results['market_bias']['Market Bias']}",
            f"Structure: {results['market_structure']['Structure']}",
            f"Supply/Demand Zone: {current_zone}",
            f"Liquidity: {results['liquidity']['Liquidity']}",
            f"BOS: {results['bos']['BOS']}",
            f"CHOCH: {results['choch']['CHoCH']}",
       ]

        # -------------------------
        # SETUP
        # -------------------------
        send_alert("Finding Setup")

        results["setup"] = setup_engine.build(results)

        # --------------------------
        # EXECUTION PLANNER
        # --------------------------
        send_alert("Preparing Execution")

        results["execution_plan"] = execution_planner.build(results)

        # --------------------------
        # EXECUTION
        # --------------------------
        send_alert("Building Execution")

        execution = execution_engine.execute(
           results["decision"], results["setup"], df["close"].iloc[-1]
       )
        results["execution"] = execution


        # -------------------------
        # RISK
        # -------------------------
        send_alert("🛡️ Calculating Risk")

        risk = None

        if results["execution"]["entry"] is not None:
            results["risk"] = risk_engine.calculate(
                execution["entry"],
                execution["stop_loss"],
                execution["take_profit"]
            )

        # -------------------------
        # NARRATIVE
        # -------------------------    
        send_alert("Generating Narrative")

        narrative = build_narrative(results)
        results["narrative"] = narrative

        # -------------------------
        # REASONING
        # -------------------------
        send_alert("🧾 Generating Reasoning")

        reasoning = reasoning_engine.explain(results)
        send_alert("✅ Analysis Complete")

        # --------------------------
        # VALIDATION
        # --------------------------

        validation = validate_analysis(results)
        results["validation"] = validation

        # --------------------------
        # BRAIN CONFIDENCE
        # --------------------------

        confidence = calculate(results)

        results["confidence"] = confidence["score"]
        results["confidence_breakdown"] = confidence["breakdown"]

        # --------------------------
        # BRAIN DECISION
        # --------------------------

        decision = decide(results)

        results["decision"] = decide(results)

        # --------------------------
        # BRAIN ADVISOR
        # --------------------------

        results["narrative"] = explain(results)

        # --------------------------
        # BRAIN RISK_MANAGER
        # --------------------------
        
        risk = check(results)

        results["trade_allowed"] = risk["trade"]
        results["risk_reason"] = risk["reason"]

        # --------------------------
        # EXECUTION QUALITY
        # --------------------------

        results["execution_quality"] = analyze_execution_quality(results)

        # --------------------------
        # WAIT SIGNAL
        # --------------------------

        results["wait_signal"] = analyze_wait_signal(results)

        # --------------------------
        # WAIT SIGNAL
        # --------------------------

        results["final_filter"] = final_filter(results)

        # --------------------------
        # WAIT SIGNAL
        # --------------------------

        results["fresh_zone"] = analyze_fresh_zone(df, supply_demand)

        results["session"] = analyze_session()

        results["trade_score"] = calculate_trade_score(results)

        results["market_memory"] = update_market_memory(results)

        results["continuation"] = analyze_continuation(
        results,
        previous_results if "previous_results" in locals() else None
        )

        results["setup_tracker"] = track_setup(results)

        results["reflection"] = reflect(results)

        results["improvements"] = analyze_improvements(results)

        results["strengths"] = analyze_strengths(results)

        results["watchlist"] = analyze_watchlist(results)

        # -------------------------
        # BUILD CHECKLIST
        # -------------------------
        
        results["checklist"] = build_checklist(results)

        # --------------------------
        # TRADE JOURNAL
        # --------------------------
        send_alert("Journalling")

        results["reasoning"] = reasoning

        journal.save(results)

        # --------------------------
        # TRADE MEMORY
        # --------------------------
        send_alert("Updating Memory")

        memory.record(results)

        results["historical_probability"] = memory.historical_probability(results)

        adaptive = adaptive_engine.calculate(

            results["confidence"],

            results["historical_probability"]
        )

        results["adaptive_confidence"] = adaptive

        results["adaptive_recommendation"] = (

        adaptive_engine.recommendation(adaptive)

        )

        results["coach"] = CoachEngine().advise(results)
        
        results["coach_summary"] = CoachEngine().summary(results)

        results["best_conditions"] = memory.best_conditions()

        results["worst_conditions"] = memory.worst_conditions()

        records = memory.load()

        records = memory.load()

        results["behaviour"] = behavior_engine.analyze(
            records
        )

        results["behaviour_recommendation"] = (

        behavior_engine.recommendation(

             results["behaviour"]

        )
        )

        records = memory.load()

        results["trader_dna"] = dna_engine.analyze(
            records
        )

        results["dna_summary"] = dna_engine.summary(
            results["trader_dna"]
        )

        records = memory.load()

        results["strategy_evolution"] = (

            evolution_engine.analyze(

                records
            )
        )

        results["strongest_strategy"] = (

            evolution_engine.strongest(

        results["strategy_evolution"]
            )
        )

    



        results["weakest_strategy"] = (

            evolution_engine.weakest(

        results["strategy_evolution"]
            )
        )

        records = memory.load()

        results["timeline"] = replay_studio.latest(records)

        results["last_trade"] = replay_studio.replay(

            records,

            len(records) - 1

        )

        results["intelligence"] = (

        intelligence.summarize(results)

        )

        results["intelligence_score"] = (

            intelligence.score(results)

        )

        results["final_recommendation"] = (

            intelligence.recommendation(

        results["intelligence_score"]

            )
        )

        filters = {

            "bias": results["market_bias"]["Market Bias"],

            "zone": results["supply_demand"]["Current Zone"],

            "liquidity": results["liquidity"]["Liquidity"]

        }

        results["replay_matches"] = replay_engine.search(
            records,
            filters
        )

        results["replay_statistics"] = replay_engine.statistics(
            results["replay_matches"]
        )

        results["patterns"] = pattern_engine.analyze(
            results["replay_matches"]
        )

        results["strongest_pattern"] = (

        pattern_engine.strongest_pattern(

            results["replay_matches"]
        )
        )

    



        results["weakest_pattern"] = (

        pattern_engine.weakest_pattern(

            results["replay_matches"]
        )
        )

        # -------------------------
        # SAVE ANALYSIS
        # -------------------------
        send_alert("Saving 🧾")

        save_analysis(symbol, results)

        # -------------------------
        # SEND REPORT
        # -------------------------
        send_alert("Reporting 🧾")

        results["report"] = build_report(results)

        # -------------------------
        # SEND VERDICT
        # -------------------------
        send_alert("Verdicting 🛡️")

        results["verdict"] = build_verdict(results["report"])

        # -------------------------
        # BUILD SUMMARY
        # -------------------------
        send_alert("Summarizing 🧾")

        results["summary"] = build_summary(results)

        # -------------------------
        # ADDING HISTORY
        # -------------------------
        send_alert("Adding History 🧾")

        add_history(results)

        # -------------------------------
        # COMPARISON OF PREVIOUS RESULTS
        # -------------------------------
        send_alert("Comparing 🧾")

        previous_results = previous()

        results["changes"] = compare(
            results,
            previous_results
       )

        # -------------------------------
        # UPDATING OF PREVIOUS RESULTS
        # -------------------------------
        send_alert("Updating 🧾")

        update_session(results)

        results["session"] = session()

        # -------------------------------
        # PERFORMANCE UPDATING
        # -------------------------------
        send_alert("Updating Performance 🧾")

        success()

        results["engine_stats"] = stats()

        return results

    finally:
     disconnect_mt5()
     send_alert("🔌 MT5 Disconnected")