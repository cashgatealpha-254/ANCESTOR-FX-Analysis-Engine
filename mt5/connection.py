import MetaTrader5 as mt5

CONNECTED = False


def connect_mt5():
    global CONNECTED

    if CONNECTED:
        return True

    if not mt5.initialize():
        print("MT5 initialization failed")
        return False

    CONNECTED = True
    print("MT5 Connected")
    return True


def disconnect_mt5():
    global CONNECTED

    if CONNECTED:
        mt5.shutdown()
        CONNECTED = False
        print("MT5 Disconnected")