class RiskEngine:

    def calculate(self, entry, stop_loss, take_profit):

        if entry is None:
            return None

        risk = abs(entry - stop_loss)
        reward = abs(take_profit - entry)

        rr = round(reward / risk, 2)

        return {
            "Risk": risk,
            "Reward": reward,
            "RR": rr
        }