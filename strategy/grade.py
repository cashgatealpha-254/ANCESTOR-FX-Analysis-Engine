class GradeEngine:

    def __init__(self):
        pass

    def grade(self, confidence):

        if confidence >= 95:
            return "A+"

        elif confidence >= 90:
            return "A"

        elif confidence >= 80:
            return "B"

        elif confidence >= 70:
            return "C"

        return "NO TRADE"