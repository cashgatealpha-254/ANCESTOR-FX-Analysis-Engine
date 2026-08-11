from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from engine.analyze import run_analysis
from engine.account import get_account_info
from engine.positions import get_positions
from engine.dashboard import dashboard_analysis
from engine.health_check import run as health_check

from mt5.connection import connect_mt5, disconnect_mt5
from charts.plot_chart import create_chart

from memory.history import (
    get_symbol_history,
    get_recent_history,
    average_confidence,
)

from environment.deep_context_store import DeepContextStore


app = FastAPI(
    title="Market Analysis Engine"
)

templates = Jinja2Templates(
    directory="templates"
)

deep_context_store = DeepContextStore()


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "status": "running",
        "engine": "Market Analysis Engine",
        "pairs": [
            "GBPUSD",
            "XAUUSD",
            "EURUSD",
            "USDJPY",
        ]
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return health_check()


# ============================================================
# DASHBOARD
# ============================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(request: Request):

    health = health_check()

    connected = connect_mt5()

    # --------------------------------------------------------
    # OFFLINE STATE
    # --------------------------------------------------------

    if not connected:

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "request": request,
                "connected": False,
                "account": {},
                "positions": [],
                "signals": [],
                "chart": None,
                "analysis": {},
                "execution_plan": None,
                "narrative": "MT5 connection unavailable.",
                "reasoning": None,
                "confidence": 0,
                "grade": "NO TRADE",
                "decision": "IGNORE",
                "trend": {},
                "market_bias": {},
                "market_state": {},
                "market_structure": {},
                "bos": {},
                "choch": {},
                "risk": None,
                "history": [],
                "current_time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "brain_status": build_brain_status(),
                "deep_context": build_deep_context_status(),
                "health": health
            }
        )

    try:

        # ----------------------------------------------------
        # ACCOUNT / POSITIONS
        # ----------------------------------------------------

        account = get_account_info()

        positions = get_positions()

        # ----------------------------------------------------
        # DASHBOARD SIGNALS
        # ----------------------------------------------------

        signals = dashboard_analysis()

        # ----------------------------------------------------
        # MAIN ANALYSIS
        # ----------------------------------------------------

        analysis = run_analysis(
            "GBPUSD"
        )

        if not isinstance(
            analysis,
            dict
        ):
            analysis = {}

        # ----------------------------------------------------
        # CHART
        # ----------------------------------------------------

        chart = create_chart(
            "GBPUSD"
        )

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        history = get_recent_history(
            10
        )

        # ----------------------------------------------------
        # NORMALIZED VALUES
        # ----------------------------------------------------

        execution_plan = analysis.get(
            "execution_plan"
        )

        risk = analysis.get(
            "risk"
        )

        narrative = analysis.get(
            "narrative",
            "No narrative available."
        )

        reasoning = analysis.get(
            "reasoning"
        )

        confidence = analysis.get(
            "confidence",
            0
        )

        grade = analysis.get(
            "grade",
            "NO TRADE"
        )

        decision = analysis.get(
            "decision",
            "IGNORE"
        )

        trend = analysis.get(
            "trend",
            {}
        )

        market_bias = analysis.get(
            "market_bias",
            {}
        )

        market_state = analysis.get(
            "market_state",
            {}
        )

        market_structure = analysis.get(
            "market_structure",
            {}
        )

        bos = analysis.get(
            "bos",
            {}
        )

        choch = analysis.get(
            "choch",
            {}
        )

        # ----------------------------------------------------
        # DASHBOARD CONTEXT
        # ----------------------------------------------------

        context = {

            "request": request,

            "connected": True,

            "account": account,

            "positions": positions,

            "signals": signals,

            "chart": chart,

            "analysis": analysis,

            "execution_plan": execution_plan,

            "risk": risk,

            "narrative": narrative,

            "reasoning": reasoning,

            "confidence": confidence,

            "grade": grade,

            "decision": decision,

            "trend": trend,

            "market_bias": market_bias,

            "market_state": market_state,

            "market_structure": market_structure,

            "bos": bos,

            "choch": choch,

            "history": history,

            "current_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "brain_status":
                build_brain_status(),

            "deep_context":
                build_deep_context_status(),

            "health": health
        }

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context=context
        )

    finally:

        disconnect_mt5()


# ============================================================
# ANALYSIS API
# ============================================================

@app.get("/analysis/{symbol}")
def analyze(symbol: str):

    return run_analysis(
        symbol.upper()
    )


# ============================================================
# HISTORY API
# ============================================================

@app.get("/history/{symbol}")
def history(symbol: str):

    history_data = get_symbol_history(
        symbol
    )

    return {
        "symbol": symbol.upper(),
        "history": history_data
    }


@app.get("/recent_history")
def recent_history(
    n: int = 10
):

    history_data = get_recent_history(
        n
    )

    return {
        "recent_history": history_data
    }


@app.get(
    "/average_confidence/{symbol}"
)
def average_confidence_endpoint(
    symbol: str
):

    avg_confidence = average_confidence(
        symbol
    )

    return {
        "symbol": symbol.upper(),
        "average_confidence": avg_confidence
    }


# ============================================================
# BRAIN STATUS
# ============================================================

def build_brain_status():

    health = health_check()

    checks = health.get(
        "checks",
        {}
    )

    return [

        {
            "name": "MT5 Connection",
            "status": (
                "READY"
                if checks.get("mt5")
                else "OFFLINE"
            ),
        },

        {
            "name": "Market Analysis",
            "status": (
                "READY"
                if checks.get("analysis")
                else "ERROR"
            ),
        },

        {
            "name": "Strategy",
            "status": (
                "READY"
                if checks.get("strategy")
                else "ERROR"
            ),
        },

        {
            "name": "Brain",
            "status": (
                "READY"
                if checks.get("brain")
                else "ERROR"
            ),
        },

        {
            "name": "Context Validation",
            "status": "READY",
        },

        {
            "name": "Context Storage",
            "status": "READY",
        },

        {
            "name": "90-Day Deep Analysis",
            "status": "RUNNING",
        },

        {
            "name": "Fast-Forward Learning",
            "status": "STANDBY",
        },

        {
            "name": "Auto Execution",
            "status": "DISABLED",
        },
    ]


# ============================================================
# DEEP CONTEXT STATUS
# ============================================================

def build_deep_context_status():

    symbols = [
        "GBPUSD",
        "XAUUSD",
        "EURUSD",
        "USDJPY",
        "DE30",
    ]

    horizons = [
        "SWING",
        "INTRADAY",
        "SCALPING",
    ]

    contexts = []

    for symbol in symbols:

        for horizon in horizons:

            exists = deep_context_store.exists(
                symbol,
                horizon
            )

            contexts.append({

                "symbol": symbol,

                "horizon": horizon,

                "status": (
                    "STORED"
                    if exists
                    else "WAITING"
                )
            })

    return contexts