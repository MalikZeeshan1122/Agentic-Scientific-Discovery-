"""
Safety & Human Approval Agent
Evaluates candidate toxicity, biosecurity risks, and manages human-in-the-loop approval gates.
"""

from typing import Dict, Any, List
from omnigent_harness.safety_policies import OmnigentSafetyPolicy

class SafetyAgent:
    """Agent responsible for biosecurity gating, toxicity filtering, and human scientist approval workflow."""

    def __init__(self, agent_id: str = "safety_approval_agent"):
        self.agent_id = agent_id
        self.policy_engine = OmnigentSafetyPolicy()

    def run(self, experiment_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Evaluates safety policies for each candidate experiment result."""
        safety_reviews = []
        for res in experiment_results:
            is_safe, warnings, rec = self.policy_engine.evaluate_candidate_safety(res)
            safety_reviews.append({
                "candidate_id": res.get("candidate_id"),
                "name": res.get("name"),
                "is_safe": is_safe,
                "warning_flags": warnings,
                "recommendation": rec,
                "requires_human_approval": not is_safe,
                "human_approval_status": "PENDING_REVIEW" if not is_safe else "APPROVED_BY_POLICY"
            })
        return safety_reviews
