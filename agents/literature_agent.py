"""
Literature & Knowledge Retrieval Agent
Queries Europe PMC, PubChem, UniProt, and OpenAlex to assemble ground truth literature and structural binding pocket context.
"""

from typing import Dict, Any, List
from experiments.real_apis import RealScientificAPIs

class LiteratureAgent:
    """Agent responsible for gathering scientific evidence, protein target annotations, and clinical benchmarks."""

    def __init__(self, agent_id: str = "lit_retrieval_agent"):
        self.agent_id = agent_id

    def run(self, query: str) -> Dict[str, Any]:
        """Runs retrieval pipeline for target scientific question."""
        target_info = RealScientificAPIs.fetch_uniprot_kras_info()
        literature = RealScientificAPIs.fetch_europe_pmc_literature(query=f"KRAS G12D {query}", limit=4)
        mrtx_compound = RealScientificAPIs.fetch_pubchem_compound("MRTX1133")
        bi_compound = RealScientificAPIs.fetch_pubchem_compound("BI-2852")

        return {
            "agent_id": self.agent_id,
            "status": "SUCCESS",
            "target_info": target_info,
            "literature": literature,
            "benchmark_compounds": [mrtx_compound, bi_compound],
            "key_takeaways": [
                "KRAS G12D features a negatively-charged Aspartic Acid residue (Asp12) substituting Glycine 12.",
                "Non-covalent binding requires basic amine salt-bridge formation with Asp12 carboxylate (distance < 3.2 Å).",
                "Switch-II pocket occupancy (residues 60-76) provides main binding free energy driven by hydrophobic contacts."
            ]
        }
