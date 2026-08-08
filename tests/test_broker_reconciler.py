import MetaTrader5 as mt5

from execution.broker_reconciler import BrokerReconciler


def main():

    if not mt5.initialize():

        print(
            "MT5 initialization failed"
        )

        return

    reconciler = BrokerReconciler()

    result = reconciler.reconcile(
        symbol="EURUSD",
        trade_id="TEST_TRADE",
        magic=123456
    )

    print(
        "Reconciliation result:"
    )

    print(result)

    mt5.shutdown()


if __name__ == "__main__":
    main()