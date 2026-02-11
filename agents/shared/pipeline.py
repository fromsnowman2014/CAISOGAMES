"""
Simple pipeline runner for composing agent analyses.
Runs agents sequentially, passes output paths between steps.

Usage:
    from agents.shared.pipeline import AgentPipeline
    from agents.design_agent.agent import DesignAgent
    from agents.code_agent.agent import CodeAgent

    pipeline = AgentPipeline()
    pipeline.add("design", DesignAgent)
    pipeline.add("code", CodeAgent)
    results = pipeline.run("games/feeding-caiso/index.html")
"""

import time
from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class PipelineStep:
    agent_name: str
    agent_class: type
    kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineResult:
    steps: List[Dict[str, Any]]
    total_time: float
    reports: List[str]


class AgentPipeline:
    """Run multiple agents in sequence on a game file."""

    def __init__(self):
        self.steps: List[PipelineStep] = []

    def add(self, name: str, agent_class: type, **kwargs) -> "AgentPipeline":
        """Add an agent to the pipeline. Returns self for chaining."""
        self.steps.append(PipelineStep(name, agent_class, kwargs))
        return self

    def run(self, game_path: str) -> PipelineResult:
        """Execute all agents in sequence and collect results."""
        results = []
        reports = []
        start = time.time()

        for step in self.steps:
            step_start = time.time()
            print(f"\n{'='*50}")
            print(f"  [{step.agent_name.upper()}] Starting...")
            print(f"{'='*50}")

            try:
                agent = step.agent_class(**step.kwargs)

                if hasattr(agent, "analyze"):
                    report_path = agent.analyze(game_path)
                elif hasattr(agent, "run"):
                    report_path = agent.run(game_path, use_simulation=True)
                else:
                    report_path = "N/A"

                elapsed = time.time() - step_start
                results.append({
                    "agent": step.agent_name,
                    "status": "success",
                    "report": report_path,
                    "time": elapsed,
                })
                reports.append(report_path)
                print(f"  [{step.agent_name.upper()}] Done ({elapsed:.1f}s) -> {report_path}")

            except Exception as e:
                elapsed = time.time() - step_start
                results.append({
                    "agent": step.agent_name,
                    "status": "error",
                    "error": str(e),
                    "time": elapsed,
                })
                print(f"  [{step.agent_name.upper()}] FAILED ({elapsed:.1f}s): {e}")

        return PipelineResult(
            steps=results,
            total_time=time.time() - start,
            reports=reports,
        )
