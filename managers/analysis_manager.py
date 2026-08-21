class AnalysisManager:
    def generate(self, score_manager, current_bpm):
        accuracy = score_manager.accuracy()
        miss = score_manager.miss
        combo = score_manager.max_combo
        perfect = score_manager.perfect
        good = score_manager.good

        if accuracy >= 90:
            overall = "Excellent"
        elif accuracy >= 75:
            overall = "Good"
        elif accuracy >= 60:
            overall = "Basic"
        else:
            overall = "Needs Practice"

        reaction = min(100, int(accuracy + perfect * 0.5))
        stability = min(100, int(accuracy + combo * 0.3))
        fatigue = max(0, min(100, int(miss * 12 + current_bpm * 0.4)))

        if fatigue < 35:
            fatigue_level = "Low"
        elif fatigue < 70:
            fatigue_level = "Medium"
        else:
            fatigue_level = "High"

        if accuracy >= 90 and miss <= 2:
            advice = "Excellent control. Continue current rhythm training."
        elif miss >= 5:
            advice = "Reduce rhythm speed and focus on stable hand movement."
        elif combo < 8:
            advice = "Try shorter sessions and improve continuous control."
        elif current_bpm >= 80 and accuracy < 75:
            advice = "Current speed may be too fast. Lower BPM is recommended."
        else:
            advice = "Good progress. Keep regular gentle training."

        return {
            "overall": overall,
            "accuracy": accuracy,
            "reaction": reaction,
            "stability": stability,
            "fatigue": fatigue_level,
            "fatigue_score": fatigue,
            "perfect": perfect,
            "good": good,
            "miss": miss,
            "max_combo": combo,
            "advice": advice
        }