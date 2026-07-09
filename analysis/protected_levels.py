def detect_protected_levels(memory):

    protected_high = memory["Latest High"]
    protected_low = memory["Latest Low"]

    return {
        "Protected High": protected_high,
        "Protected Low": protected_low
    }