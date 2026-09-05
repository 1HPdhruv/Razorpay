import numpy as np
import uuid
from typing import List, Dict, Any
from app.models.simulation import Scenario, SimulationResult
from app.models.pattern import Pattern
from app.services.simulation.safety import enforce_safety_policy

class CounterfactualEngine:
    def simulate(self, pattern: Pattern, scenario: Scenario, matched_transactions: List[Dict[str, Any]], runs: int = 1000, seed: int = 42) -> SimulationResult:
        enforce_safety_policy({"scenario_id": scenario.scenario_id})
        
        np.random.seed(seed)
        
        total_observed_loss = 0
        loss_tx_count = 0
        non_loss_tx_count = 0
        
        for tx in matched_transactions:
            if tx['loss_flag']:
                total_observed_loss += tx['loss_amount']
                loss_tx_count += 1
            else:
                non_loss_tx_count += 1
                
        # loss_amount in synthetic data is already in paise (it copies amount_paise).
        observed_loss_paise = int(total_observed_loss)
        
        # losses array for each loss transaction in paise
        losses_array = np.array([int(tx['loss_amount']) for tx in matched_transactions if tx['loss_flag']])
        
        if len(losses_array) == 0:
            return self._build_result(pattern, scenario, matched_transactions, observed_loss_paise, 0, 0, 0, 0, runs, seed)
            
        # Shape: (runs, number_of_loss_tx)
        # Random matrix where True means the intervention was successful
        success_matrix = np.random.rand(runs, len(losses_array)) < scenario.effectiveness
        
        # Prevented losses in each run
        prevented_losses_per_run = np.sum(success_matrix * losses_array, axis=1)
        
        p10 = int(np.percentile(prevented_losses_per_run, 10))
        median = int(np.percentile(prevented_losses_per_run, 50))
        p90 = int(np.percentile(prevented_losses_per_run, 90))
        
        estimated_prevented_loss_paise = median
        estimated_residual_loss_paise = observed_loss_paise - estimated_prevented_loss_paise
        
        # Costing
        total_tx = len(matched_transactions)
        intervention_cost_paise = total_tx * scenario.cost_model.intervention_cost_paise
        
        # False positives are non-loss transactions that were intervened upon
        false_positive_cost_paise = non_loss_tx_count * scenario.cost_model.false_positive_cost_paise
        
        net_benefit_paise = estimated_prevented_loss_paise - intervention_cost_paise - false_positive_cost_paise
        
        return self._build_result(
            pattern=pattern,
            scenario=scenario,
            matched_transactions=matched_transactions,
            observed_loss_paise=observed_loss_paise,
            estimated_prevented_loss_paise=estimated_prevented_loss_paise,
            estimated_residual_loss_paise=estimated_residual_loss_paise,
            intervention_cost_paise=intervention_cost_paise,
            false_positive_cost_paise=false_positive_cost_paise,
            net_benefit_paise=net_benefit_paise,
            p10=p10, median=median, p90=p90,
            runs=runs, seed=seed
        )

    def _build_result(self, pattern, scenario, matched_transactions, observed_loss_paise, estimated_prevented_loss_paise, estimated_residual_loss_paise, intervention_cost_paise, false_positive_cost_paise, net_benefit_paise, p10, median, p90, runs, seed):
        
        # Recommendation Logic
        if pattern.p_value > 0.05 or pattern.matching_transaction_count < 10:
            recommendation = "REQUIRE_MANUAL_REVIEW"
        elif net_benefit_paise < 0:
            recommendation = "DO_NOT_INTERVENE"
        else:
            recommendation = "RECOMMEND_INTERVENTION"
            
        prevention_rate = estimated_prevented_loss_paise / observed_loss_paise if observed_loss_paise > 0 else 0.0
            
        return SimulationResult(
            simulation_id=f"SIM_{uuid.uuid4().hex[:8]}",
            pattern_id=pattern.pattern_id,
            scenario_id=scenario.scenario_id,
            transactions_evaluated=len(matched_transactions),
            observed_loss_paise=observed_loss_paise,
            estimated_prevented_loss_paise=estimated_prevented_loss_paise,
            estimated_residual_loss_paise=estimated_residual_loss_paise,
            intervention_cost_paise=intervention_cost_paise,
            false_positive_cost_paise=false_positive_cost_paise,
            net_estimated_benefit_paise=net_benefit_paise,
            prevention_rate=prevention_rate,
            assumption_effectiveness=scenario.effectiveness,
            simulation_runs=runs,
            confidence_interval={"p10": p10, "median": median, "p90": p90},
            limitations=["Simulation assumes effectiveness probability.", "Does not guarantee real-world user conversion drops."],
            recommendation=recommendation
        )
