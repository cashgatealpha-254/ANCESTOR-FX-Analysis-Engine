# engine/history.py

from collections import deque

# Stores the last 20 analyses
_history = deque(maxlen=20)


def add(results):
    """
    Save latest analysis.
    """
    _history.append(results)


def latest():
    """
    Return latest analysis.
    """
    if not _history:
        return None

    return _history[-1]


def previous():
    """
    Return previous analysis.
    """
    if len(_history) < 2:
        return None

    return _history[-2]


def all():
    """
    Return history.
    """
    return list(_history)