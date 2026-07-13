def detect_protected_levels(memory):

    if memory["Trend"] == "Bullish":

        protected_high = None
        protected_low = memory["Latest Low"]

    elif memory["Trend"] == "Bearish":

        protected_high = memory["Latest High"]
        protected_low = None

    else:

        protected_high = None
        protected_low = None

    return {
        "Protected High": protected_high,
        "Protected Low": protected_low
    }