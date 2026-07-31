from datetime import datetime


def analyze_session():

    hour = datetime.now().hour

    if 0 <= hour < 8:
        session = "Asian"

    elif 8 <= hour < 16:
        session = "London"

    else:
        session = "New York"

    return {
        "Session": session
    }