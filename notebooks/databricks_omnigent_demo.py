"""
Databricks Omnigent Managed Sandbox Quickstart Notebook
Run this file inside Databricks Omnigent environment (<workspace-url>/omnigent -> New Session -> Sandbox)
"""

import sys
import os
import json

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from omnigent_harness.meta_harness import OmnigentMetaHarness
from agents.literature_agent import LiteratureAgent
from agents.hypothesis_agent import HypothesisAgent
from agents.experiment_agent import ExperimentAgent
from agents.safety_agent import SafetyAgent
from agents.analysis_agent import AnalysisAgent

def main():
    print("=" * 80)
    print("  OMNIGENT META-HARNESS DEMO: AGENTIC SCIENTIFIC DISCOVERY (KRAS G12D)")
    print("  7th Global AI Hackathon - Databricks x Hack-Nation")
    print("=" * 80)

    # Resolve config path relative to project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, "omnigent_config.yaml")

    # Initialize Harness
    harness = OmnigentMetaHarness(config_path=config_path)

    # Register Specialist Agents
    harness.register_agent("lit_retrieval_agent", LiteratureAgent())
    harness.register_agent("hypothesis_formulator_agent", HypothesisAgent())
    harness.register_agent("computational_experiment_agent", ExperimentAgent())
    harness.register_agent("safety_approval_agent", SafetyAgent())
    harness.register_agent("analysis_decision_agent", AnalysisAgent())

    # Scientific Question
    question = "Discover novel non-covalent KRAS G12D binders and PROTAC degraders targeting Asp12 salt bridges and Switch-II pockets."

    # Execute Discovery Loop
    results = harness.run_discovery_loop(question)

    print("\n[+] DISCOVERY LOOP COMPLETE!")
    print(f"Session ID: {results['session_id']}")
    print(f"Top Lead Candidate: {results['top_candidate']['name']} (Kd = {results['top_candidate']['experimental_results']['kd_nanomolar']} nM)")
    print(f"Discovery Acceleration Multiplier: {results['speedup_metrics']['metric_label']}")
    print(f"Next Scientific Experiment: {results['next_experiment']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
