import time
import json
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent, AgentDecision
from task_graph import TaskGraph, TaskGraphBuilder

class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="Planner",
            role="Task Planning and DAG Generation"
        )

    async def execute(self, input_data: Dict[str, Any],
                     context: Optional[Dict[str, Any]] = None) -> AgentDecision:
        start_time = time.time()

        task_description = input_data.get("task_description", "")

        try:
            task_graph = TaskGraphBuilder.parse_task(task_description)

            is_valid, errors = task_graph.validate_dag()

            if not is_valid:
                raise ValueError(f"Invalid DAG: {errors}")

            stages = task_graph.get_parallel_stages()

            reasoning = f"Analyzed task: '{task_description[:50]}...'. "
            reasoning += f"Generated DAG with {len(task_graph.nodes)} nodes in {len(stages)} stages. "
            reasoning += f"Identified parallelizable operations for efficiency."

            decision_data = {
                "task_graph_id": task_graph.id,
                "task_graph": task_graph.to_dict(),
                "num_nodes": len(task_graph.nodes),
                "stages": stages,
                "stage_count": len(stages),
            }

            execution_time = time.time() - start_time
            decision = AgentDecision(
                agent_name=self.name,
                decision="DAG_GENERATED",
                reasoning=reasoning,
                confidence=0.95,
                execution_time=execution_time,
                data=decision_data
            )

            self.record_decision(decision)
            self.execution_count += 1

            return decision

        except Exception as e:
            execution_time = time.time() - start_time
            error_decision = AgentDecision(
                agent_name=self.name,
                decision="PLANNING_FAILED",
                reasoning=f"Failed to generate plan: {str(e)}",
                confidence=0.0,
                execution_time=execution_time,
            )
            self.record_decision(error_decision)
            self.execution_count += 1

            return error_decision
