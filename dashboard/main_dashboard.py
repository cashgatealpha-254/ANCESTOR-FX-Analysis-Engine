from dashboard.header import show as show_header
from dashboard.market_snapshot import show as show_snapshot
from dashboard.decision_card import show as show_decision
from dashboard.execution_card import show as show_execution
from dashboard.reasoning_card import show as show_reasoning
from dashboard.risk_card import show as show_risk
from dashboard.engine_status import show as show_engine


def display(results):

    show_header(results["symbol"], results["health"])

    show_snapshot(results)

    show_decision(
        results["report"],
        results["verdict"]
    )

    show_execution(results["report"])

    show_reasoning(results["report"])

    show_risk(results)

    show_engine(results)