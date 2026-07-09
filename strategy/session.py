from datetime import datetime


class SessionEngine:

    def __init__(self):
        pass

    def current_session(self):

        hour = datetime.utcnow().hour

        if 0 <= hour < 7:
            return "ASIAN"

        elif 7 <= hour < 16:
            return "LONDON"

        elif 12 <= hour < 21:
            return "NEW YORK"

        return "CLOSED"