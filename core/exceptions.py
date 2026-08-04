class AncestorError(Exception):
    """Base exception for Ancestor."""
    pass


class MT5ConnectionError(AncestorError):
    pass


class CandleDataError(AncestorError):
    pass


class IndicatorError(AncestorError):
    pass


class StrategyError(AncestorError):
    pass


class MemoryError(AncestorError):
    pass


class RiskError(AncestorError):
    pass


class NotificationError(AncestorError):
    pass


def handle_exception(e):

    return {

        "status": "error",

        "type": type(e).__name__,

        "message": str(e)

    }