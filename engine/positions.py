import MetaTrader5 as mt5


def get_positions():
    """
    Returns all currently open MT5 positions.
    """

    positions = mt5.positions_get()

    if positions is None:
        return []

    open_positions = []

    for position in positions:

        trade = {
            "ticket": position.ticket,
            "symbol": position.symbol,
            "type": "BUY" if position.type == mt5.ORDER_TYPE_BUY else "SELL",
            "volume": position.volume,
            "entry": position.price_open,
            "current_price": position.price_current,
            "sl": position.sl,
            "tp": position.tp,
            "profit": position.profit
        }

        open_positions.append(trade)

    return open_positions