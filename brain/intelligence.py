class IntelligenceCore:

    def __init__(self):
        pass

    def summarize(self, results):

        return {

            "Decision":

                results.get("decision"),

            "Confidence":

                results["adaptive_confidence"]["Adaptive Confidence"],

            "Behaviour":

                results["behaviour"]["Behaviour Score"],

            "DNA":

                results["trader_dna"]["Trading Style"],

            "Strongest Strategy":

                results["strongest_strategy"],

            "Coach":

                results["coach_summary"]

        }

    def score(self, results):

        confidence = results["adaptive_confidence"]["Adaptive Confidence"]

        behaviour = results["behaviour"]["Behaviour Score"]

        score = (

            confidence * 0.7 +

            behaviour * 0.3

        )

        return round(score, 2)

    def recommendation(self, score):

        if score >= 90:

            return "Execute"

        elif score >= 80:

            return "High Conviction"

        elif score >= 65:

            return "Wait For Confirmation"

        elif score >= 50:

            return "Observe"

        return "Stand Aside"