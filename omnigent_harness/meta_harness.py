"""
Omnigent Meta-Harness Core Orchestrator
Manages multi-agent execution, cross-agent message handoffs, sandbox policies, state logging, and session traces.
"""

import time
import yaml
import json
import logging
from typing import Dict, Any, List, Callable
from .safety_policies import OmnigentSafetyPolicy
from .acceleration_metrics import AccelerationMetricsCalculator

logger = logging.getLogger(__name__)

class OmnigentMetaHarness:
    """Core meta-harness orchestrator for managing specialist agents in scientific discovery."""

    def __init__(self, config_path: str = "omnigent_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.safety_policy = OmnigentSafetyPolicy(
            spend_cap=self.config.get("harness", {}).get("spend_cap_usd", 50.0),
            require_human_gate=self.config.get("governance", {}).get("human_in_the_loop", True)
        )
        self.session_id = f"omnigent-session-{int(time.time())}"
        self.trace_logs = []
        self.registered_agents = {}
        self.shared_research_record = {
            "session_id": self.session_id,
            "target": "KRAS G12D (PDB: 6W4E)",
            "iterations": [],
            "literature_corpus": [],
            "hypotheses": [],
            "experiments": [],
            "safety_reviews": [],
            "decisions": []
        }

    def _load_config(self) -> Dict[str, Any]:
        """Loads harness config YAML file."""
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load config file {self.config_path}: {e}")
            return {"harness": {"name": "OmniDiscovery-Lab"}}

    def register_agent(self, agent_id: str, agent_instance: Any):
        """Registers a specialist agent in the harness topology."""
        self.registered_agents[agent_id] = agent_instance
        self.log_trace("SYSTEM", f"Agent registered in Omnigent topology: {agent_id}")

    def log_trace(self, agent_id: str, message: str, payload: Dict[str, Any] = None):
        """Records an agent event trace in the shared research record."""
        entry = {
            "timestamp": time.strftime("%H:%M:%S"),
            "agent_id": agent_id,
            "message": message,
            "payload": payload or {}
        }
        self.trace_logs.append(entry)

    def run_discovery_loop(self, user_question: str) -> Dict[str, Any]:
        """
        Executes one complete Omnigent multi-agent discovery loop:
          1. Literature & Knowledge Agent -> Gather context & benchmarks
          2. Hypothesis Formulator Agent -> Generate candidate SMILES & mechanisms
          3. Computational Experiment Agent -> Execute docking & ADMET screens
          4. Safety & Human Approval Agent -> Evaluate biosecurity & toxicity risk
          5. Analysis & Decision Agent -> Interpret results & formulate next step
        """
        start_time = time.time()
        self.log_trace("OMNIGENT_ORCHESTRATOR", f"Initiating 24-Hour Scientific Discovery Loop for question: '{user_question}'")

        # Step 1: Literature & Knowledge Agent
        lit_agent = self.registered_agents.get("lit_retrieval_agent")
        lit_results = lit_agent.run(user_question) if lit_agent else {}
        self.shared_research_record["literature_corpus"] = lit_results.get("literature", [])
        self.log_trace("LITERATURE_AGENT", "Aggregated PubMed/Europe PMC publications & PDB: 6W4E crystal structure context.", lit_results)

        # Step 2: Hypothesis Formulator Agent
        hypo_agent = self.registered_agents.get("hypothesis_formulator_agent")
        hypo_results = hypo_agent.run(lit_results) if hypo_agent else {}
        self.shared_research_record["hypotheses"] = hypo_results.get("hypotheses", [])
        self.log_trace("HYPOTHESIS_AGENT", f"Formulated {len(hypo_results.get('candidates', []))} novel candidate chemical hypotheses.", hypo_results)

        # Step 3: Computational Experiment Agent
        exp_agent = self.registered_agents.get("computational_experiment_agent")
        candidates = hypo_results.get("candidates", [])
        exp_results = exp_agent.run(candidates) if exp_agent else []
        self.shared_research_record["experiments"] = exp_results
        self.log_trace("EXPERIMENT_AGENT", f"Completed docking, Kd estimation, & ADMET screening for {len(exp_results)} candidates.", {"count": len(exp_results)})

        # Step 4: Safety & Human Approval Agent
        safety_agent = self.registered_agents.get("safety_approval_agent")
        safety_reviews = safety_agent.run(exp_results) if safety_agent else []
        self.shared_research_record["safety_reviews"] = safety_reviews
        self.log_trace("SAFETY_AGENT", "Evaluated biosecurity, hERG cardiotoxicity, AMES mutagenicity, and SA scores.", {"reviews": safety_reviews})

        # Step 5: Analysis & Decision Agent
        analysis_agent = self.registered_agents.get("analysis_decision_agent")
        decision_results = analysis_agent.run(exp_results, safety_reviews) if analysis_agent else {}
        self.shared_research_record["decisions"].append(decision_results)
        self.log_trace("ANALYSIS_AGENT", f"Synthesized findings. Formulated next scientific experiment: {decision_results.get('next_experiment_title')}", decision_results)

        elapsed = time.time() - start_time
        speedup = AccelerationMetricsCalculator.calculate_speedup_metrics(
            num_candidates_screened=len(exp_results),
            iteration_count=1,
            elapsed_seconds_omnigent=elapsed
        )

        return {
            "session_id": self.session_id,
            "target": "KRAS G12D (PDB: 6W4E)",
            "user_question": user_question,
            "research_record": self.shared_research_record,
            "trace_logs": self.trace_logs,
            "speedup_metrics": speedup,
            "top_candidate": decision_results.get("top_lead_candidate"),
            "next_experiment": decision_results.get("next_experiment_title")
        }
