import json
import time
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

from task_graph import TaskGraph, TaskGraphBuilder, TaskNode, NodeType, NodeStatus
from execution_engine import ExecutionEngine
from memory.memory_system import MemorySystem
from notion.notion_client import NotionClient, NotionMCPAdapter
from tools.tools_interface import ToolManager
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.researcher import ResearcherAgent
from agents.critic_agents import QualityCritic, CreativityCritic, PracticalityCritic
from utils.logger import get_logger

class NotionOSXOrchestrator:

    def __init__(self, memory_dir: str = "memory"):
        self.logger = get_logger()
        self.memory_system = MemorySystem(memory_dir)
        self.tool_manager = ToolManager()
        self.notion_client = NotionClient()
        self.notion_adapter = NotionMCPAdapter(self.notion_client)

        self.planner = PlannerAgent()
        self.executor = ExecutorAgent(self.tool_manager)
        self.researcher = ResearcherAgent(self.tool_manager)
        self.critics = [
            QualityCritic(),
            CreativityCritic(),
            PracticalityCritic(),
        ]

        self.execution_history: List[Dict[str, Any]] = []

    async def process_task(self, task_description: str) -> Dict[str, Any]:
        task_id = f"task_{int(time.time())}"

        self.logger.info(
            "Orchestrator",
            f"Starting task processing: {task_description[:50]}...",
            {"task_id": task_id}
        )

        try:
            self.logger.info("Orchestrator", "STEP 1: Generating execution plan")
            plan_decision = await self.planner.execute({
                "task_description": task_description
            })

            if plan_decision.decision != "DAG_GENERATED":
                raise Exception(f"Planning failed: {plan_decision.reasoning}")

            task_graph = TaskGraph(task_description)
            task_graph.id = plan_decision.data["task_graph_id"]

            from task_graph import NodeType, NodeStatus

            for node_id, node_data in plan_decision.data.get("nodes", {}).items():
                node_type_str = node_data.get("type", "execute")
                node_type = NodeType(node_type_str) if isinstance(node_type_str, str) else node_type_str

                status_str = node_data.get("status", "pending")
                status = NodeStatus(status_str) if isinstance(status_str, str) else status_str

                node = TaskNode(
                    id=node_id,
                    name=node_data.get("name", ""),
                    description=node_data.get("description", ""),
                    node_type=node_type,
                    status=status,
                    dependencies=node_data.get("dependencies", []),
                    estimated_duration=node_data.get("estimated_duration", 5.0),
                )
                task_graph.nodes[node_id] = node

            self.logger.info(
                "Orchestrator",
                "Plan generated",
                {
                    "nodes": len(task_graph.nodes),
                    "stages": plan_decision.data["stage_count"]
                }
            )

            self.logger.info("Orchestrator", "STEP 2: Conducting research")
            research_decision = await self.researcher.execute({
                "task_description": task_description,
                "research_query": task_description
            })

            self.logger.info(
                "Orchestrator",
                "Research completed",
                {"sources": research_decision.data["research_data"]["results_count"]}
            )

            self.logger.info("Orchestrator", "STEP 3: Executing task graph")
            execution_summary = await self._execute_task_graph(task_graph)

            self.logger.info("Orchestrator", "STEP 4: Running critic evaluations")
            critic_scores = await self._run_critics(execution_summary)

            self.logger.info("Orchestrator", "STEP 5: Analyzing improvement opportunities")
            needs_improvement, improvement_strategy = self._analyze_scores(critic_scores)

            final_output = execution_summary
            if needs_improvement:
                self.logger.info(
                    "Orchestrator",
                    "STEP 6: Applying refinements",
                    {"strategy": improvement_strategy}
                )
                final_output = await self._refine_output(
                    execution_summary,
                    critic_scores,
                    improvement_strategy
                )

                refined_scores = await self._run_critics(final_output)

                for critic_name, old_score in critic_scores.items():
                    new_score = refined_scores.get(critic_name, old_score)
                    if new_score > old_score:
                        self.memory_system.feedback.record_improvement(
                            task_id,
                            critic_name,
                            old_score,
                            new_score,
                            improvement_strategy
                        )

            self.logger.info("Orchestrator", "STEP 7: Requesting human approval")
            output_summary = self._generate_output_summary(final_output)
            approved = await self.notion_adapter.request_approval(task_id, output_summary)

            if approved:
                self.logger.info("Orchestrator", "Task approved by human reviewer")
                await self.notion_adapter.finalize_task(task_id)
            else:
                self.logger.warning("Orchestrator", "Task was rejected")

            self.logger.info("Orchestrator", "STEP 8: Recording in memory system")
            self.memory_system.episodic.record_task(
                task_id,
                task_description,
                final_output,
                "COMPLETED" if approved else "REJECTED",
                time.time() - time.time()
            )

            self.memory_system.strategy.store_strategy(
                strategy_name=f"approach_for_{improvement_strategy}",
                description=task_description,
                effectiveness=sum(critic_scores.values()) / len(critic_scores),
                context={"task": task_description}
            )

            return {
                "task_id": task_id,
                "status": "COMPLETED" if approved else "REJECTED",
                "output": final_output,
                "critic_scores": critic_scores,
                "approved": approved,
                "execution_summary": execution_summary,
            }

        except Exception as e:
            self.logger.error(
                "Orchestrator",
                f"Task processing failed: {str(e)}"
            )
            raise

    async def _execute_task_graph(self, task_graph: TaskGraph) -> Dict[str, Any]:
        async def node_executor(node: TaskNode) -> Any:
            executor_input = {
                "node_id": node.id,
                "node_description": node.description,
                "tools": [],
            }

            decision = await self.executor.execute(executor_input)
            return decision.data

        engine = ExecutionEngine(task_graph)
        summary = await engine.execute_dag(node_executor)
        return summary

    async def _run_critics(self, output: Dict[str, Any]) -> Dict[str, float]:
        scores = {}

        for critic in self.critics:
            decision = await critic.execute({
                "output": output
            })

            score = decision.data.get("score", 0.0) if decision.data else 0.0
            scores[critic.name] = score

            self.logger.info(
                "Orchestrator",
                f"Critic {critic.name} scored",
                {"score": score, "feedback": decision.data.get("feedback", "")}
            )

        return scores

    def _analyze_scores(self, critic_scores: Dict[str, float]) -> tuple[bool, str]:
        avg_score = sum(critic_scores.values()) / len(critic_scores)
        threshold = 0.7

        if avg_score < threshold:
            min_score_critic = min(critic_scores, key=critic_scores.get)
            return True, min_score_critic

        return False, ""

    async def _refine_output(self, output: Dict[str, Any],
                            scores: Dict[str, float],
                            strategy: str) -> Dict[str, Any]:
        self.logger.info("Orchestrator", f"Refining output using strategy: {strategy}")

        refined = output.copy()
        refined["refinement_applied"] = strategy
        refined["iteration"] = refined.get("iteration", 0) + 1

        return refined

    def _generate_output_summary(self, output: Dict[str, Any]) -> str:
        summary = "TASK EXECUTION SUMMARY\n"
        summary += "=" * 60 + "\n"

        if "output" in output:
            summary += f"Output: {str(output['output'])[:200]}\n"
        if "total_execution_time" in output:
            summary += f"Execution Time: {output['total_execution_time']:.2f}s\n"
        if "completed" in output:
            summary += f"Nodes Completed: {output['completed']}/{output['total_nodes']}\n"

        summary += "=" * 60 + "\n"
        return summary

    def get_system_status(self) -> Dict[str, Any]:
        return {
            "agents": {
                "planner": self.planner.get_stats(),
                "executor": self.executor.get_stats(),
                "researcher": self.researcher.get_stats(),
                "critics": [c.get_stats() for c in self.critics],
            },
            "memory": self.memory_system.get_summary(),
            "tasks_processed": len(self.execution_history),
            "notion_tasks": self.notion_client.get_task_summary(),
        }

    def print_status(self):
        status = self.get_system_status()

        print("\n" + "=" * 80)
        print("NOTIONOS X SYSTEM STATUS")
        print("=" * 80)

        print("\nAGENT STATISTICS:")
        print(f"  Planner: {status['agents']['planner']['execution_count']} executions")
        print(f"  Executor: {status['agents']['executor']['execution_count']} executions")
        print(f"  Researcher: {status['agents']['researcher']['execution_count']} executions")

        print("\nCRITIC STATISTICS:")
        for critic_stat in status['agents']['critics']:
            print(f"  {critic_stat['name']}: {critic_stat['execution_count']} evaluations")

        print("\nMEMORY SYSTEM:")
        for key, val in status['memory'].items():
            print(f"  {key}: {val}")

        print("\nTASKS:")
        print(f"  Total processed: {status['tasks_processed']}")
        print(f"  In Notion: {status['notion_tasks']['total']}")

        print("=" * 80 + "\n")
