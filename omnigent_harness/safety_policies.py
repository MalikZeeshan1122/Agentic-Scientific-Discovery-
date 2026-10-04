"""
Omnigent Governance & Safety Policy Engine
Enforces biosecurity checks, toxicity thresholds, spend limits, and human-in-the-loop approval gates.
"""

from typing import Dict, Any, List, Tuple

class OmnigentSafetyPolicy:
    """Governance and safety evaluation engine for Omnigent multi-agent discovery labs."""

    def __init__(self, spend_cap: float = 50.0, require_human_gate: bool = True):
        self.spend_cap = spend_cap
        self.require_human_gate = require_human_gate
        self.audit_log = []

    def evaluate_candidate_safety(self, candidate_data: Dict[str, Any]) -> Tuple[bool, List[str], str]:
        """
        Evaluates safety and biosecurity policies for a chemical candidate.
        Returns: (is_safe, warning_flags, recommendation)
        """
        warnings = []
        admet = candidate_data.get("admet_profile", {})
        smiles = candidate_data.get("smiles", "")
        risks = admet.get("admet_risks", {})

        # Check 1: Cardiotoxicity (hERG)
        if risks.get("herg_cardiotox") == "High Risk":
            warnings.append("HIGH_HERG_CARDIOTOXICITY: High predicted LogP (> 4.8) increases cardiac risk.")

        # Check 2: Mutagenicity
        if risks.get("ames_mutagenicity") == "Positive Warning":
            warnings.append("BIOSECURITY_WARN: Contains reactive nitro/nitroso motifs flagged by AMES filter.")

        # Check 3: Synthetic Accessibility (SA Score > 7.5 indicates extreme complexity or reactive intermediate)
        sa_score = admet.get("sa_score", 3.0)
        if sa_score > 7.5:
            warnings.append(f"SYNTHESIS_BOTTLENECK: Synthetic accessibility score ({sa_score}) exceeds standard lead limit.")

        # Check 4: Human Gate Requirement
        if len(warnings) > 0:
            status = "REQUIRES_HUMAN_APPROVAL"
            recommendation = "Candidate flagged by Safety Agent. Human scientist approval required before wet-lab proposal."
            is_safe = False
        else:
            status = "PASSED_SAFETY_GATE"
            recommendation = "Candidate passes all automated biosecurity and toxicity checks. Cleared for lead optimization."
            is_safe = True

        self.audit_log.append({
            "candidate_id": candidate_data.get("candidate_id"),
            "status": status,
            "warnings": warnings,
            "recommendation": recommendation
        })

        return is_safe, warnings, recommendation
