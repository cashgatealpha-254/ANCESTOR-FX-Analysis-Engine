import MetaTrader5 as mt5


def get_account_info():

    info = mt5.account_info()

    if info is None:
        return {
            "status": "Disconnected",
            "message": "No MT5 account connected."
        }

    return {
        "status": "Connected",
        "login": info.login,
        "server": info.server,
        "balance": info.balance,
        "equity": info.equity,
        "profit": info.profit,
        "margin": info.margin,
        "free_margin": info.margin_free,
        "margin_level": info.margin_level,
        "leverage": info.leverage,
        "currency": info.currency,
        "name": info.name
    }