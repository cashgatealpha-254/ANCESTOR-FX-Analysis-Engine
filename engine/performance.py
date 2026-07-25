# engine/performance.py

from datetime import datetime

_performance = {
    "total_analyses": 0,
    "successful_runs": 0,
    "failed_runs": 0,
    "last_run": None
}


def success():

    _performance["total_analyses"] += 1
    _performance["successful_runs"] += 1
    _performance["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def failure():

    _performance["total_analyses"] += 1
    _performance["failed_runs"] += 1
    _performance["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def stats():

    success_rate = 0

    if _performance["total_analyses"] > 0:
        success_rate = (
            _performance["successful_runs"]
            /
            _performance["total_analyses"]
        ) * 100

    return {
        **_performance,
        "success_rate": round(success_rate, 2)
    }