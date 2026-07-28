# confluence.py

from engine.trend import get_trend
from engine.structure import get_structure
from engine.liquidity import get_liquidity
from engine.supply_demand import get_supply_demand
from engine.session import get_session


def calculate_confluence(symbol):

    trend = get_trend(symbol)

    structure = get_structure(symbol)

    liquidity = get_liquidity(symbol)

    zones = get_supply_demand(symbol)

    session = get_session()

    score = (
        trend["score"]
        + structure["score"]
        + liquidity["score"]
        + zones["score"]
        + session["score"]
    )

    confidence = min(score, 100)

    if confidence >= 90:
        grade = "A"
        decision = "EXECUTE"

    elif confidence >= 70:
        grade = "B"
        decision = "WAIT"

    else:
        grade = "C"
        decision = "NO TRADE"

    return {
        "confidence": confidence,
        "grade": grade,
        "decision": decision,
        "modules": {
            "trend": trend,
            "structure": structure,
            "liquidity": liquidity,
            "zones": zones,
            "session": session,
        },
    }