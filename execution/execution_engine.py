import MetaTrader5 as mt5

from execution.execution_registry import ExecutionRegistry
from execution.broker_reconciler import BrokerReconciler


class ExecutionEngine:

    def __init__(
        self,
        risk_engine,
        position_sizer,
        magic=260807
    ):

        self.risk_engine = risk_engine
        self.position_sizer = position_sizer

        self.magic = int(magic)

        self.registry = ExecutionRegistry()

        self.reconciler = BrokerReconciler()

    # ==================================================
    # EXECUTE
    # ==================================================

    def execute(
        self,
        setup,
        dry_run=True
    ):

        # ------------------------------------------------
        # 1. BASIC SETUP VALIDATION
        # ------------------------------------------------

        if not isinstance(
            setup,
            dict
        ):

            return self._blocked(
                "Invalid setup"
            )

        symbol = setup.get(
            "symbol"
        )

        if not symbol:

            return self._blocked(
                "Missing symbol"
            )

        # ------------------------------------------------
        # 2. MT5 CONNECTION
        # ------------------------------------------------

        if not mt5.terminal_info():

            return self._error(
                symbol,
                "MT5 terminal unavailable"
            )

        # ------------------------------------------------
        # 3. RISK ENGINE
        # ------------------------------------------------

        risk = self.risk_engine.validate(
            setup
        )

        if not isinstance(
            risk,
            dict
        ):

            return self._error(
                symbol,
                "Risk engine returned invalid result"
            )

        if risk.get(
            "status"
        ) != "ALLOW":

            return {

                "status": "BLOCKED",

                "stage": "RISK",

                "symbol": symbol,

                "reason": risk.get(
                    "reason",
                    "Risk validation failed"
                ),

                "risk": risk
            }

        # ------------------------------------------------
        # 4. POSITION SIZING
        # ------------------------------------------------

        sizing = self.position_sizer.calculate(
            risk
        )

        if not isinstance(
            sizing,
            dict
        ):

            return self._error(
                symbol,
                "Position sizer returned invalid result"
            )

        if sizing.get(
            "status"
        ) != "READY":

            return {

                "status": "BLOCKED",

                "stage": "POSITION_SIZE",

                "symbol": symbol,

                "reason": sizing.get(
                    "reason",
                    "Position sizing failed"
                ),

                "sizing": sizing
            }

        volume = sizing.get(
            "volume"
        )

        if volume is None:

            return self._error(
                symbol,
                "Position volume unavailable"
            )

        try:

            volume = float(
                volume
            )

        except (
            TypeError,
            ValueError
        ):

            return self._error(
                symbol,
                "Invalid position volume"
            )

        if volume <= 0:

            return self._blocked(
                "Position volume is zero"
            )

        # ------------------------------------------------
        # 5. BUILD UNIQUE TRADE ID
        # ------------------------------------------------

        trade_id = (
            self.registry.build_trade_id(
                setup
            )
        )

        if not trade_id:

            return self._blocked(
                "Unable to build trade identity"
            )

        # ------------------------------------------------
        # 6. DUPLICATE CHECK
        # ------------------------------------------------

        existing = self.registry.get(
            trade_id
        )

        if existing:

            return {

                "status": "BLOCKED",

                "stage": "REGISTRY",

                "symbol": symbol,

                "trade_id": trade_id,

                "reason": (
                    "Trade already exists "
                    "in execution registry"
                ),

                "existing": existing
            }

        # ------------------------------------------------
        # 7. BROKER RECONCILIATION
        # ------------------------------------------------

        reconciliation = (
            self.reconciler.reconcile(
                symbol=symbol,
                trade_id=trade_id,
                magic=self.magic
            )
        )

        if reconciliation.get(
            "status"
        ) in {
            "FILLED",
            "PENDING"
        }:

            return {

                "status": "BLOCKED",

                "stage": "RECONCILIATION",

                "symbol": symbol,

                "trade_id": trade_id,

                "reason": (
                    "Matching broker trade "
                    "already exists"
                ),

                "reconciliation": reconciliation
            }

        if reconciliation.get(
            "status"
        ) == "UNKNOWN":

            return {

                "status": "BLOCKED",

                "stage": "RECONCILIATION",

                "symbol": symbol,

                "trade_id": trade_id,

                "reason": (
                    "Broker state could not "
                    "be determined safely"
                ),

                "reconciliation": reconciliation
            }

        # ------------------------------------------------
        # 8. DRY RUN GATE
        # ------------------------------------------------

        if dry_run:

            return {

                "status": "DRY_RUN",

                "stage": "READY_FOR_BROKER",

                "symbol": symbol,

                "trade_id": trade_id,

                "volume": volume,

                "risk": risk,

                "sizing": sizing,

                "message": (
                    "All execution gates passed. "
                    "No order was sent."
                )
            }

        # ------------------------------------------------
        # 9. REGISTER SUBMITTING
        # ------------------------------------------------

        registered = self.registry.register(

            trade_id=trade_id,

            status="SUBMITTING",

            setup=setup
        )

        if registered.get(
            "status"
        ) != "REGISTERED":

            return {

                "status": "BLOCKED",

                "stage": "REGISTRY",

                "symbol": symbol,

                "trade_id": trade_id,

                "reason": (
                    "Unable to reserve "
                    "trade identity"
                )
            }

        # ------------------------------------------------
        # 10. BUILD MT5 REQUEST
        # ------------------------------------------------

        request = self._build_request(
            setup,
            volume,
            trade_id
        )

        if request is None:

            self.registry.update(
                trade_id,
                "FAILED",
                reason="Invalid MT5 request"
            )

            return {

                "status": "BLOCKED",

                "stage": "REQUEST",

                "symbol": symbol,

                "trade_id": trade_id,

                "reason": (
                    "Unable to build "
                    "broker request"
                )
            }

        # ------------------------------------------------
        # 11. BROKER PRE-CHECK
        # ------------------------------------------------

        check = mt5.order_check(
            request
        )

        if check is None:

            self.registry.update(
                trade_id,
                "UNKNOWN",
                reason=(
                    "MT5 order_check returned None"
                )
            )

            return {

                "status": "UNKNOWN",

                "stage": "ORDER_CHECK",

                "symbol": symbol,

                "trade_id": trade_id,

                "reason": (
                    "Broker pre-check "
                    "returned no result"
                )
            }

        if check.retcode != mt5.TRADE_RETCODE_DONE:

            reason = (
                f"Broker rejected pre-check: "
                f"{check.retcode} "
                f"{getattr(check, 'comment', '')}"
            )

            self.registry.update(
                trade_id,
                "FAILED",
                reason=reason
            )

            return {

                "status": "BLOCKED",

                "stage": "ORDER_CHECK",

                "symbol": symbol,

                "trade_id": trade_id,

                "retcode": check.retcode,

                "reason": reason
            }

        # ------------------------------------------------
        # 12. SEND ORDER
        # ------------------------------------------------

        result = mt5.order_send(
            request
        )

        # ------------------------------------------------
        # 13. NO RESPONSE = UNKNOWN
        # ------------------------------------------------

        if result is None:

            self.registry.update(
                trade_id,
                "UNKNOWN",
                reason=(
                    "MT5 order_send returned None"
                )
            )

            return {

                "status": "UNKNOWN",

                "stage": "ORDER_SEND",

                "symbol": symbol,

                "trade_id": trade_id,

                "reason": (
                    "Broker response unavailable"
                )
            }

        # ------------------------------------------------
        # 14. SUCCESS
        # ------------------------------------------------

        if result.retcode in {
            mt5.TRADE_RETCODE_DONE,
            mt5.TRADE_RETCODE_PLACED
        }:

            ticket = getattr(
                result,
                "order",
                None
            )

            if not ticket:

                ticket = getattr(
                    result,
                    "deal",
                    None
                )

            self.registry.update(

                trade_id,

                "SUBMITTED",

                ticket=ticket,

                reason=getattr(
                    result,
                    "comment",
                    ""
                )
            )

            # ------------------------------------------------
            # 15. IMMEDIATE RECONCILIATION
            # ------------------------------------------------

            reconciled = (
                self.reconciler.reconcile(
                    symbol=symbol,
                    trade_id=trade_id,
                    magic=self.magic
                )
            )

            return {

                "status": "SUBMITTED",

                "stage": "BROKER",

                "symbol": symbol,

                "trade_id": trade_id,

                "ticket": ticket,

                "volume": volume,

                "risk": risk,

                "sizing": sizing,

                "broker_result": {
                    "retcode": result.retcode,
                    "comment": getattr(
                        result,
                        "comment",
                        ""
                    )
                },

                "reconciliation": reconciled
            }

        # ------------------------------------------------
        # 16. BROKER REJECTION
        # ------------------------------------------------

        reason = (
            f"Broker rejected order: "
            f"{result.retcode} "
            f"{getattr(result, 'comment', '')}"
        )

        self.registry.update(
            trade_id,
            "FAILED",
            reason=reason
        )

        return {

            "status": "REJECTED",

            "stage": "BROKER",

            "symbol": symbol,

            "trade_id": trade_id,

            "retcode": result.retcode,

            "reason": reason
        }

    # ==================================================
    # BUILD REQUEST
    # ==================================================

    def _build_request(
        self,
        setup,
        volume,
        trade_id
    ):

        symbol = setup.get(
            "symbol"
        )

        direction = str(
            setup.get(
                "direction",
                ""
            )
        ).upper()

        entry = setup.get(
            "entry"
        )

        stop_loss = setup.get(
            "stop_loss"
        )

        take_profit = setup.get(
            "take_profit"
        )

        if (
            not symbol
            or entry is None
            or stop_loss is None
            or take_profit is None
        ):

            return None

        symbol_info = mt5.symbol_info(
            symbol
        )

        tick = mt5.symbol_info_tick(
            symbol
        )

        if (
            symbol_info is None
            or tick is None
        ):

            return None

        if direction == "BULLISH":

            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask

        elif direction == "BEARISH":

            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid

        else:

            return None

        return {

            "action": mt5.TRADE_ACTION_DEAL,

            "symbol": symbol,

            "volume": float(
                volume
            ),

            "type": order_type,

            "price": float(
                price
            ),

            "sl": float(
                stop_loss
            ),

            "tp": float(
                take_profit
            ),

            "deviation": 20,

            "magic": self.magic,

            "comment": trade_id,

            "type_time": (
                mt5.ORDER_TIME_GTC
            ),

            "type_filling": (
                mt5.ORDER_FILLING_FOK
            )
        }

    # ==================================================
    # RESPONSE HELPERS
    # ==================================================

    @staticmethod
    def _blocked(
        reason
    ):

        return {

            "status": "BLOCKED",

            "reason": reason
        }

    @staticmethod
    def _error(
        symbol,
        reason
    ):

        return {

            "status": "ERROR",

            "symbol": symbol,

            "reason": reason
        }