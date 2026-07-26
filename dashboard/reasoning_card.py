from dashboard.theme import HEADER_REASONING, SECTION, BRAIN


def show(report):

    print(f"\n{BRAIN} {HEADER_REASONING}")
    print(SECTION)

    reason = report.get("reason")

    if isinstance(reason, list):
        for item in reason:
            print(f"• {item}")

    elif isinstance(reason, str):
        print(reason)

    else:
        print("No reasoning available.")