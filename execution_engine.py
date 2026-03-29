import asyncio
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from task_graph import TaskGraph, TaskNode, NodeStatus
from utils.logger import get_logger

@dataclass
class ExecutionResult:
    task_id: str
    node_id: str
    status: NodeStatus
    output: Any
    error: Optional[str] = None
    duration: float = 0.0

class ExecutionEngine:

    def __init__(self, task_graph: TaskGraph):
        self.task_graph = task_graph
        self.execution_results: Dict[str, ExecutionResult] = {}
        self.logger = get_logger()
        self.execution_start_time = 0.0

    async def execute_dag(self,
                         node_executor: Callable,
                         max_parallel: int = 5) -> Dict[str, Any]:
        self.execution_start_time = time.time()

        self.logger.info(
            "ExecutionEngine",
            "Starting DAG execution",
            {
                "task_id": self.task_graph.id,
                "num_nodes": len(self.task_graph.nodes),
            }
        )

        try:
            stages = self.task_graph.get_parallel_stages()

            for stage_idx, stage_nodes in enumerate(stages):
                self.logger.info(
                    "ExecutionEngine",
                    f"Executing stage {stage_idx + 1}/{len(stages)}",
                    {"nodes_in_stage": len(stage_nodes)}
                )

                tasks = []
                for node_id in stage_nodes:
                    tasks.append(self._execute_node(node_id, node_executor))

                results = await self._execute_with_semaphore(tasks, max_parallel)

                failures = [r for r in results if r.status == NodeStatus.FAILED]
                if failures:
                    self.logger.warning(
                        "ExecutionEngine",
                        f"Stage {stage_idx + 1} had failures",
                        {"failures": len(failures)}
                    )

            execution_time = time.time() - self.execution_start_time

            self.logger.info(
                "ExecutionEngine",
                "DAG execution completed",
                {
                    "total_time": execution_time,
                    "nodes_completed": len(self.execution_results),
                }
            )

            return self._generate_summary()

        except Exception as e:
            self.logger.error(
                "ExecutionEngine",
                f"DAG execution failed: {str(e)}"
            )
            raise

    async def _execute_node(self, node_id: str,
                           node_executor: Callable) -> ExecutionResult:
        node = self.task_graph.nodes[node_id]
        start_time = time.time()

        try:
            node.status = NodeStatus.IN_PROGRESS

            self.logger.debug(
                "ExecutionEngine",
                f"Executing node: {node.name}",
                {"node_id": node_id, "type": node.node_type.value}
            )

            output = await node_executor(node)

            node.status = NodeStatus.COMPLETED
            node.output = output

            duration = time.time() - start_time

            result = ExecutionResult(
                task_id=self.task_graph.id,
                node_id=node_id,
                status=NodeStatus.COMPLETED,
                output=output,
                duration=duration
            )

            self.execution_results[node_id] = result

            self.logger.info(
                "ExecutionEngine",
                f"Node completed: {node.name}",
                {"duration": duration}
            )

            return result

        except Exception as e:
            node.status = NodeStatus.FAILED
            node.error = str(e)

            duration = time.time() - start_time

            result = ExecutionResult(
                task_id=self.task_graph.id,
                node_id=node_id,
                status=NodeStatus.FAILED,
                output=None,
                error=str(e),
                duration=duration
            )

            self.execution_results[node_id] = result

            self.logger.error(
                "ExecutionEngine",
                f"Node failed: {node.name}",
                {"error": str(e)}
            )

            return result

    async def _execute_with_semaphore(self, tasks: List,
                                     max_parallel: int) -> List[ExecutionResult]:
        semaphore = asyncio.Semaphore(max_parallel)

        async def bounded_task(task):
            async with semaphore:
                return await task

        return await asyncio.gather(*[bounded_task(t) for t in tasks])

    def _generate_summary(self) -> Dict[str, Any]:
        total_time = time.time() - self.execution_start_time

        completed = sum(
            1 for r in self.execution_results.values()
            if r.status == NodeStatus.COMPLETED
        )
        failed = sum(
            1 for r in self.execution_results.values()
            if r.status == NodeStatus.FAILED
        )

        return {
            "task_id": self.task_graph.id,
            "total_nodes": len(self.task_graph.nodes),
            "completed": completed,
            "failed": failed,
            "total_execution_time": total_time,
            "status": "SUCCESS" if failed == 0 else "PARTIAL_SUCCESS",
            "execution_results": {
                nid: {
                    "status": r.status.value,
                    "output": r.output,
                    "duration": r.duration,
                    "error": r.error,
                }
                for nid, r in self.execution_results.items()
            }
        }
