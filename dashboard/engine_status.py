from dashboard.theme import HEADER_ENGINE, SECTION, ENGINE


def show(results):

    stats = results.get("engine_stats", {})

    print(f"\n{ENGINE} {HEADER_ENGINE}")
    print(SECTION)

    print(f"Runs          : {stats.get('total_analyses')}")

    print(f"Success Rate  : {stats.get('success_rate')}%")

    print(f"Last Run      : {stats.get('last_run')}")