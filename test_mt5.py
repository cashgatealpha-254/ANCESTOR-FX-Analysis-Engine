from data.fetcher import connect_mt5, disconnect_mt5, get_price

try:
    connect_mt5()

    price = get_price("GBPUSD")
    print(price)

finally:
    disconnect_mt5()