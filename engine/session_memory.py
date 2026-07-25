# engine/session_memory.py

_session = {
    "symbol": None,
    "analyses": 0,
    "last_decision": None,
    "last_confidence": None,
    "highest_confidence": 0,
}


def update(results):

    _session["symbol"] = results.get("symbol")

    _session["analyses"] += 1

    _session["last_decision"] = results.get("decision")

    _session["last_confidence"] = results.get("confidence")

    confidence = results.get("confidence", 0)

    if confidence > _session["highest_confidence"]:
        _session["highest_confidence"] = confidence


def get():

    return _session


def reset():

    _session["symbol"] = None
    _session["analyses"] = 0
    _session["last_decision"] = None
    _session["last_confidence"] = None
    _session["highest_confidence"] = 0