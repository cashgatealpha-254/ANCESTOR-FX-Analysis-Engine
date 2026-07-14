class RiskEngine:

    def calculate(self, entry, stop_loss, take_profit):

        if entry is None:
            return None

        risk = abs(entry - stop_loss)
        reward = abs(take_profit - entry)

        if risk == 0:
            rr = 0
        else:
            rr = round(reward / risk, 2)

        return {
            "Risk": round(risk, 5),
            "Reward": round(reward, 5),
            "RR": rr
        }