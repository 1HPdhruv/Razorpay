from typing import Dict, Any

class RiskDecisionEngine:
    @staticmethod
    def evaluate(pattern_confidence: float, net_benefit_paise: int, false_positive_cost_paise: int, support: int) -> Dict[str, Any]:
        """
        Synthesizes statistical confidence and counterfactual simulation results into an auditable decision.
        """
        reasons = []
        
        # 1. Base statistical confidence check
        if pattern_confidence < 0.05 or support < 10:
            reasons.append("Held-out confidence below threshold or insufficient support")
            return {
                "decision": "REQUIRE_MANUAL_REVIEW",
                "reasons": reasons
            }
            
        # 2. Financial Benefit check
        if net_benefit_paise <= 0:
            reasons.append("Estimated net benefit is zero or negative")
            return {
                "decision": "DO_NOT_INTERVENE",
                "reasons": reasons
            }
            
        # 3. False Positive Tolerance check
        # As a heuristic for the hackathon, if FP cost > 30% of prevented loss (which implies high friction), escalate.
        # But here we just compare absolute scale. If FP cost > Prevented Loss / 3 roughly.
        # For simplicity, if FP cost exceeds 100000 paise (1000 INR) randomly or based on volume, we might flag.
        if false_positive_cost_paise > (net_benefit_paise * 0.5):
            reasons.append("Estimated false-positive cost is disproportionately high")
            return {
                "decision": "REQUIRE_MANUAL_REVIEW",
                "reasons": reasons
            }
            
        reasons.append("Statistically validated pattern with positive net benefit")
        return {
            "decision": "RECOMMEND_INTERVENTION",
            "reasons": reasons
        }
