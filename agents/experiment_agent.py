"""
Computational Experimentation & Screening Agent
Runs high-throughput computational simulations, affinity docking, selectivity screens, and ADMET property evaluations.
"""

from typing import Dict, Any, List
from experiments.kras_simulation import KRASG12DSimulator

class ExperimentAgent:
    """Agent responsible for executing computational scientific experiments and collecting structured evidence."""

    def __init__(self, agent_id: str = "computational_experiment_agent"):
        self.agent_id = agent_id

    def run(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Executes simulation experiments for all generated candidates."""
        results = []
        for candidate in candidates:
            exp_result = KRASG12DSimulator.simulate_binding_experiment(candidate)
            results.append(exp_result)
        return results
