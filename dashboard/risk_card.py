from dashboard.theme import HEADER_RISK, SECTION, RISK


def show(results):

    risk = results.get("risk", {})

    print(f"\n{RISK} {HEADER_RISK}")
    print(SECTION)

    print(f"Trade Allowed : {results.get('trade_allowed')}")

    print(f"Risk %        : {risk.get('risk_percent')}")

    print(f"Lot Size      : {risk.get('lot_size')}")

    print(f"RR            : {risk.get('risk_reward')}")