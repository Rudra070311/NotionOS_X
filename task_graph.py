import json
import uuid
from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

class NodeType(Enum):
    PLAN = "plan"
    RESEARCH = "research"
    EXECUTE = "execute"
    VALIDATE = "validate"
    REVIEW = "review"
    REFINE = "refine"

class NodeStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class TaskNode:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    node_type: NodeType = NodeType.EXECUTE
    status: NodeStatus = NodeStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: float = 5.0
    output: Optional[Any] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.node_type.value,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "estimated_duration": self.estimated_duration,
            "output": self.output,
            "error": self.error,
        }

class TaskGraph:

    def __init__(self, task_description: str):
        self.id = str(uuid.uuid4())[:12]
        self.task_description = task_description
        self.nodes: Dict[str, TaskNode] = {}
        self.created_at = str(json.dumps({}))

    def add_node(self, name: str, node_type: NodeType = NodeType.EXECUTE,
                 description: str = "", dependencies: List[str] = None,
                 estimated_duration: float = 5.0) -> TaskNode:
        node = TaskNode(
            name=name,
            description=description,
            node_type=node_type,
            dependencies=dependencies or [],
            estimated_duration=estimated_duration
        )
        self.nodes[node.id] = node
        return node

    def validate_dag(self) -> tuple[bool, List[str]]:
        errors = []

        for node_id, node in self.nodes.items():
            for dep in node.dependencies:
                if dep not in self.nodes:
                    errors.append(f"Node {node_id} references non-existent dependency {dep}")

        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def has_cycle(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)

            for dep in self.nodes[node_id].dependencies:
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True

            rec_stack.remove(node_id)
            return False

        for node_id in self.nodes:
            if node_id not in visited:
                if has_cycle(node_id):
                    errors.append(f"Cycle detected involving {node_id}")

        return len(errors) == 0, errors

    def get_execution_order(self) -> List[str]:
        visited: Set[str] = set()
        order: List[str] = []

        def dfs(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)

            for dep in self.nodes[node_id].dependencies:
                dfs(dep)

            order.append(node_id)

        for node_id in self.nodes:
            dfs(node_id)

        return order

    def get_parallel_stages(self) -> List[List[str]]:
        in_degree: Dict[str, int] = {nid: 0 for nid in self.nodes}

        for node in self.nodes.values():
            for dep in node.dependencies:
                in_degree[node.id] += 1

        stages = []
        processed: Set[str] = set()

        while len(processed) < len(self.nodes):
            current_stage = []
            for node_id, node in self.nodes.items():
                if node_id not in processed:
                    unprocessed_deps = [d for d in node.dependencies if d not in processed]
                    if not unprocessed_deps:
                        current_stage.append(node_id)

            if not current_stage:
                break

            stages.append(current_stage)
            processed.update(current_stage)

        return stages

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task_description": self.task_description,
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "execution_order": self.get_execution_order(),
            "parallel_stages": self.get_parallel_stages(),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

class TaskGraphBuilder:

    @staticmethod
    def parse_task(task_description: str) -> TaskGraph:
        graph = TaskGraph(task_description)

        task_lower = task_description.lower()

        plan_node = graph.add_node(
            name="Generate Execution Plan",
            node_type=NodeType.PLAN,
            description="Analyze task and create execution strategy",
            estimated_duration=3.0
        )

        research_needed = any(kw in task_lower for kw in
                             ["research", "analyze", "find", "discover", "learn"])
        research_node = None
        if research_needed:
            research_node = graph.add_node(
                name="Research & Gather Information",
                node_type=NodeType.RESEARCH,
                description="Gather external knowledge and context",
                dependencies=[plan_node.id],
                estimated_duration=5.0
            )

        execute_deps = [research_node.id if research_node else plan_node.id]
        execute_node = graph.add_node(
            name="Execute Main Task",
            node_type=NodeType.EXECUTE,
            description="Perform the core task operations",
            dependencies=execute_deps,
            estimated_duration=8.0
        )

        validate_needed = any(kw in task_lower for kw in
                             ["validate", "test", "check", "verify", "ensure"])
        validate_node = None
        if validate_needed:
            validate_node = graph.add_node(
                name="Validate Results",
                node_type=NodeType.VALIDATE,
                description="Verify outputs meet requirements",
                dependencies=[execute_node.id],
                estimated_duration=4.0
            )

        review_deps = [validate_node.id if validate_node else execute_node.id]
        review_node = graph.add_node(
            name="Quality Review (Critics)",
            node_type=NodeType.REVIEW,
            description="Multiple critic agents score the output",
            dependencies=review_deps,
            estimated_duration=6.0
        )

        refine_node = graph.add_node(
            name="Refinement (if needed)",
            node_type=NodeType.REFINE,
            description="Apply critic feedback and improve output",
            dependencies=[review_node.id],
            estimated_duration=5.0
        )

        return graph
