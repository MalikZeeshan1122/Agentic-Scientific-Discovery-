"""
ADMET & Pharmacophore Molecular Property Evaluator
Calculates Lipinski Rule of 5 parameters, synthetic accessibility (SA) score, and toxicity risks.
"""

import math
import re
from typing import Dict, Any

class ADMETCalculator:
    """Computes medicinal chemistry physical properties, drug-likeness, and ADMET toxicity indicators."""

    @staticmethod
    def evaluate_smiles(smiles: str, mw: float, logp: float, tpsa: float) -> Dict[str, Any]:
        """Assess drug-likeness according to Lipinski Rule of 5 and Veber rules."""

        # Count hydrogen bond donors and acceptors from SMILES string heuristics
        hbd = len(re.findall(r'\[NH\d*\]|NH|OH|\[OH\]', smiles))
        hba = len(re.findall(r'N|O|F', smiles)) - hbd
        hba = max(1, hba)
        rotatable_bonds = max(1, len(re.findall(r'-|#', smiles)) // 2 + smiles.count('CC'))

        # Lipinski Violations
        violations = []
        if mw > 500:
            violations.append("MW > 500 Da")
        if logp > 5.0:
            violations.append("LogP > 5.0")
        if hbd > 5:
            violations.append("HBD > 5")
        if hba > 10:
            violations.append("HBA > 10")

        lipinski_pass = len(violations) <= 1
        veber_pass = (tpsa <= 140) and (rotatable_bonds <= 10)

        # Synthetic Accessibility (SA Score 1-10, where lower is easier to synthesize)
        # Heuristic based on ring counts, molecular weight, and heteroatom complexity
        num_rings = smiles.count('1') + smiles.count('2') + smiles.count('3')
        sa_score = round(min(9.5, max(1.5, 2.0 + (mw / 150.0) + (num_rings * 0.4) - (0.2 * hbd))), 2)

        # Toxicity Risk Prediction (hERG cardiotoxicity, hepatotoxicity, AMES mutagenicity)
        herg_risk = "Low" if logp < 4.0 else ("Moderate" if logp < 4.8 else "High Risk")
        hepatotox_risk = "Low" if (tpsa > 60 and logp < 4.2) else "Moderate"
        ames_mutagenicity = "Negative" if "N(=O)=O" not in smiles and "NN" not in smiles else "Positive Warning"

        overall_drug_likeness = "High" if (lipinski_pass and veber_pass and sa_score < 6.0) else (
            "Moderate" if (lipinski_pass or veber_pass) else "Low / Lead Optimization Required"
        )

        return {
            "smiles": smiles,
            "mw": mw,
            "logp": logp,
            "tpsa": tpsa,
            "hbd": hbd,
            "hba": hba,
            "rotatable_bonds": rotatable_bonds,
            "lipinski_violations": len(violations),
            "violation_details": violations,
            "lipinski_compliant": lipinski_pass,
            "veber_compliant": veber_pass,
            "sa_score": sa_score,
            "admet_risks": {
                "herg_cardiotox": herg_risk,
                "hepatotoxicity": hepatotox_risk,
                "ames_mutagenicity": ames_mutagenicity
            },
            "drug_likeness_rating": overall_drug_likeness
        }
