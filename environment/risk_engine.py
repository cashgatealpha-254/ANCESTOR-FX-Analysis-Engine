import MetaTrader5 as mt5


class RiskEngine:

    def __init__(
        self,
        risk_percent=1.0,
        max_risk_percent=2.0,
        minimum_rr=2.0
    ):

        self.risk_percent = float(
            risk_percent
        )

        self.max_risk_percent = float(
            max_risk_percent
        )

        self.minimum_rr = float(
            minimum_rr
        )

    # ==================================================
    # VALIDATE SETUP
    # ==================================================

    def validate(
        self,
        setup
    ):

        if not isinstance(
            setup,
            dict
        ):

            return {
                "status": "BLOCKED",
                "reason": "Invalid setup"
            }

        if setup.get(
            "status"
        ) != "READY":

            return {
                "status": "BLOCKED",
                "reason": "Setup is not READY"
            }

        symbol = setup.get(
            "symbol"
        )

        entry = setup.get(
            "entry"
        )

        stop_loss = setup.get(
            "stop_loss"
        )

        take_profit = setup.get(
            "take_profit"
        )

        direction = str(
            setup.get(
                "direction",
                ""
            )
        ).upper()

        # ==================================================
        # BASIC VALIDATION
        # ==================================================

        if not symbol:

            return {
                "status": "BLOCKED",
                "reason": "Missing symbol"
            }

        if direction not in {
            "BULLISH",
            "BEARISH"
        }:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Invalid direction"
            }

        if (
            entry is None
            or stop_loss is None
            or take_profit is None
        ):

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Incomplete trade levels"
            }

        try:

            entry = float(entry)
            stop_loss = float(stop_loss)
            take_profit = float(take_profit)

        except (
            TypeError,
            ValueError
        ):

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Invalid trade levels"
            }

        # ==================================================
        # DIRECTION / LEVEL VALIDATION
        # ==================================================

        if direction == "BULLISH":

            if not (
                stop_loss < entry < take_profit
            ):

                return {
                    "status": "BLOCKED",
                    "symbol": symbol,
                    "reason": (
                        "Invalid bullish "
                        "entry/SL/TP structure"
                    )
                }

        else:

            if not (
                take_profit < entry < stop_loss
            ):

                return {
                    "status": "BLOCKED",
                    "symbol": symbol,
                    "reason": (
                        "Invalid bearish "
                        "entry/SL/TP structure"
                    )
                }

        # ==================================================
        # RISK / REWARD
        # ==================================================

        risk_distance = abs(
            entry - stop_loss
        )

        reward_distance = abs(
            take_profit - entry
        )

        if risk_distance <= 0:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Zero risk distance"
            }

        rr = (
            reward_distance
            / risk_distance
        )

        if rr < self.minimum_rr:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "rr": round(rr, 2),
                "reason": (
                    f"RR {rr:.2f} below "
                    f"minimum {self.minimum_rr:.2f}"
                )
            }

        # ==================================================
        # RISK LIMIT
        # ==================================================

        if (
            self.risk_percent <= 0
            or self.risk_percent
            > self.max_risk_percent
        ):

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": (
                    "Configured risk exceeds "
                    "allowed risk limit"
                )
            }

        # ==================================================
        # ACCOUNT INFORMATION
        # ==================================================

        account = mt5.account_info()

        if account is None:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Unable to retrieve "
                    "MT5 account information"
                )
            }

        balance = float(
            account.balance
        )

        equity = float(
            account.equity
        )

        if equity <= 0:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Invalid account equity"
            }

        # ==================================================
        # MONEY AT RISK
        # ==================================================

        money_at_risk = (
            equity
            * self.risk_percent
            / 100.0
        )

        # ==================================================
        # SYMBOL INFORMATION
        # ==================================================

        symbol_info = mt5.symbol_info(
            symbol
        )

        if symbol_info is None:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": (
                    "Symbol information unavailable"
                )
            }

        point = float(
            symbol_info.point
        )

        if point <= 0:

            return {
                "status": "ERROR",
                "symbol": symbol,
                "reason": "Invalid symbol point size"
            }

        # ==================================================
        # DISTANCE IN POINTS
        # ==================================================

        risk_points = (
            risk_distance
            / point
        )

        if risk_points <= 0:

            return {
                "status": "BLOCKED",
                "symbol": symbol,
                "reason": "Invalid risk points"
            }

        # ==================================================
        # RESULT
        # ==================================================

        return {

            "status": "ALLOW",

            "symbol": symbol,

            "direction": direction,

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "risk_distance": risk_distance,

            "reward_distance": reward_distance,

            "risk_points": risk_points,

            "rr": round(
                rr,
                2
            ),

            "risk_percent": (
                self.risk_percent
            ),

            "money_at_risk": round(
                money_at_risk,
                2
            ),

            "balance": balance,

            "equity": equity,

            "point": point
        }