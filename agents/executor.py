import time
import json
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent, AgentDecision
from tools.tools_interface import ToolManager

class ExecutorAgent(BaseAgent):

    def __init__(self, tool_manager: Optional[ToolManager] = None):
        super().__init__(
            name="Executor",
            role="Task Execution and Tool Management"
        )
        self.tool_manager = tool_manager or ToolManager()
        self.tool_calls = []

    async def execute(self, input_data: Dict[str, Any],
                     context: Optional[Dict[str, Any]] = None) -> AgentDecision:
        start_time = time.time()

        node_id = input_data.get("node_id", "unknown")
        node_description = input_data.get("node_description", "")
        tools_to_use = input_data.get("tools", [])

        try:
            execution_results = []

            for tool_spec in tools_to_use:
                tool_result = await self.tool_manager.execute_tool(
                    tool=tool_spec.get("tool"),
                    method=tool_spec.get("method"),
                    **tool_spec.get("params", {})
                )

                execution_results.append({
                    "tool": tool_spec.get("tool"),
                    "method": tool_spec.get("method"),
                    "result": tool_result.to_dict()
                })

                self.tool_calls.append({
                    "node_id": node_id,
                    "tool": tool_spec.get("tool"),
                    "method": tool_spec.get("method"),
                    "success": tool_result.success,
                })

            task_output = self._generate_output(
                node_description,
                execution_results
            )

            reasoning = f"Executed task '{node_description[:40]}...'. "
            if tools_to_use:
                reasoning += f"Invoked {len(tools_to_use)} tools successfully. "
            reasoning += "Generated output for next stage."

            decision_data = {
                "node_id": node_id,
                "execution_results": execution_results,
                "output": task_output,
                "tools_used": len(tools_to_use),
            }

            execution_time = time.time() - start_time
            decision = AgentDecision(
                agent_name=self.name,
                decision="EXECUTION_COMPLETE",
                reasoning=reasoning,
                confidence=0.9,
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
                decision="EXECUTION_FAILED",
                reasoning=f"Task execution failed: {str(e)}",
                confidence=0.0,
                execution_time=execution_time,
            )
            self.record_decision(error_decision)
            self.execution_count += 1

            return error_decision

    @staticmethod
    def _generate_output(task_description: str, results: list) -> dict:
        summary = f"Completed: {task_description}\n"
        summary += f"Executed {len(results)} tool calls.\n"

        success_count = sum(
            1 for r in results if r["result"].get("success", False)
        )

        summary += f"Success rate: {success_count}/{len(results)} calls"

        return {
            "summary": summary,
            "execution_results": results,
            "success_count": success_count,
            "total_operations": len(results),
        }
