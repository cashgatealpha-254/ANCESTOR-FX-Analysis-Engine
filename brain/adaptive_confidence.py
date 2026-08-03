class AdaptiveConfidence:

    def __init__(self,
                 confidence_weight=0.70,
                 history_weight=0.30):

        self.confidence_weight = confidence_weight
        self.history_weight = history_weight

    def calculate(self,
                  current_confidence,
                  historical_results):

        historical_confidence = historical_results.get(
            "Probability",
            0
        )

        sample_size = historical_results.get(
            "Sample Size",
            0
        )

        wins = historical_results.get(
            "Wins",
            0
        )

        losses = historical_results.get(
            "Losses",
            0
        )

        adaptive_confidence = (

            current_confidence * self.confidence_weight +

            historical_confidence * self.history_weight

        )

        if sample_size < 10:

            adaptive_confidence *= 0.95

        elif sample_size < 25:

            adaptive_confidence *= 0.98

        elif sample_size >= 100:

            adaptive_confidence *= 1.02

        adaptive_confidence = max(

            0,

            min(

                100,

                round(adaptive_confidence, 2)

            )

        )

        if adaptive_confidence >= 90:

            level = "Exceptional"

        elif adaptive_confidence >= 80:

            level = "High"

        elif adaptive_confidence >= 65:

            level = "Moderate"

        elif adaptive_confidence >= 50:

            level = "Low"

        else:

            level = "Very Low"

        return {

            "Current Confidence": current_confidence,

            "Historical Confidence": historical_confidence,

            "Adaptive Confidence": adaptive_confidence,

            "Confidence Level": level,

            "Sample Size": sample_size,

            "Wins": wins,

            "Losses": losses,

            "Confidence Weight": self.confidence_weight,

            "History Weight": self.history_weight

        }

    def recommendation(self,
                       adaptive_results):

        confidence = adaptive_results["Adaptive Confidence"]

        if confidence >= 90:

            return "Maximum conviction. Execute if risk rules allow."

        elif confidence >= 80:

            return "High quality setup."

        elif confidence >= 65:

            return "Valid setup. Normal execution."

        elif confidence >= 50:

            return "Proceed with caution."

        return "Avoid trade. Wait for better confirmation."