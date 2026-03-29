import json
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class DAGOptimization:
    parallelizable_nodes: int
    critical_path_length: int
    estimated_speedup: float
    bottleneck_nodes: List[str]
    parallelization_opportunities: int


class PlannerV2:
    
    def __init__(self):
        self.cache = {}
        self.optimization_history = []
        
    def plan_task_advanced(self, task: str, context: Dict = None) -> Dict:
        logger.info(f"🧠 [Planner V2] Planning task: {task[:50]}...")
        
        # Parse task into components
        components = self._extract_task_components(task)
        
        # Build initial DAG
        dag, nodes_map = self._build_dag(components)
        
        # Analyze DAG structure
        analysis = self._analyze_dag_structure(dag)
        
        optimized_dag = self._optimize_for_parallelism(dag, analysis)
        
        plan = self._create_execution_plan(optimized_dag, components)
        
        logger.info(f"✅ Generated DAG with {len(plan['nodes'])} nodes, "
                   f"parallelism factor: {analysis.parallelization_opportunities}")
        
        return plan
    
    def _extract_task_components(self, task: str) -> List[Dict]:
        components = []
        
        subtasks = [
            "Analyze requirements",
            "Research solutions",
            "Design architecture",
            "Implement core",
            "Test implementation",
            "Document results",
            "Generate report"
        ]
        
        for i, subtask in enumerate(subtasks):
            if i == 0:
                dependencies = []
            elif i in [1, 2]:
                dependencies = [0]
            elif i == 3:
                dependencies = [1, 2]
            elif i in [4, 5]:
                dependencies = [3]
            else:
                dependencies = [4, 5]
                
            components.append({
                "id": f"component_{i}",
                "description": subtask,
                "complexity": self._estimate_complexity(subtask),
                "dependencies": [f"component_{d}" for d in dependencies],
                "estimated_duration_ms": self._estimate_duration(subtask)
            })
        
        return components
    
    def _build_dag(self, components: List[Dict]) -> Tuple[Dict, Dict]:
        nodes = {}
        edges = []
        
        for component in components:
            nodes[component["id"]] = {
                "id": component["id"],
                "description": component["description"],
                "complexity": component["complexity"],
                "estimated_duration_ms": component["estimated_duration_ms"],
                "type": "task",
                "status": "pending"
            }
            
            for dep in component["dependencies"]:
                edges.append({"from": dep, "to": component["id"]})
        
        return {"nodes": nodes, "edges": edges}, nodes
    
    def _analyze_dag_structure(self, dag: Dict) -> DAGOptimization:
        nodes = dag["nodes"]
        edges = dag["edges"]
        

        in_degree = {nid: 0 for nid in nodes}
        out_degree = {nid: 0 for nid in nodes}
        
        for edge in edges:
            out_degree[edge["from"]] += 1
            in_degree[edge["to"]] += 1
        

        parallel_groups = self._find_parallel_groups(edges, nodes)
        

        critical_path = self._find_critical_path(dag)
        

        bottlenecks = [nid for nid, out in out_degree.items() 
                      if out > 3 or in_degree[nid] > 3]
        
        return DAGOptimization(
            parallelizable_nodes=len(parallel_groups),
            critical_path_length=len(critical_path),
            estimated_speedup=len(parallel_groups) / max(len(critical_path), 1),
            bottleneck_nodes=bottlenecks,
            parallelization_opportunities=len(parallel_groups) * 2
        )
    
    def _find_parallel_groups(self, edges: List, nodes: Dict) -> List[List]:
        groups = []
        

        dep_map = {}
        for nid in nodes:
            deps = tuple(sorted([e["from"] for e in edges if e["to"] == nid]))
            if deps not in dep_map:
                dep_map[deps] = []
            dep_map[deps].append(nid)
        

        groups = [nodes for nodes in dep_map.values() if len(nodes) > 1]
        
        return groups
    
    def _find_critical_path(self, dag: Dict) -> List[str]:
        nodes = dag["nodes"]
        edges = dag["edges"]
        

        

        start_nodes = [nid for nid in nodes 
                      if not any(e["to"] == nid for e in edges)]
        

        if not start_nodes:
            return []
        
        max_path = self._build_longest_path(start_nodes[0], nodes, edges, set())
        
        return max_path
    
    def _build_longest_path(self, node_id: str, nodes: Dict, 
                           edges: List, visited: Set) -> List[str]:
        if node_id in visited:
            return [node_id]
        
        visited.add(node_id)
        

        successors = [e["to"] for e in edges if e["from"] == node_id]
        
        if not successors:
            return [node_id]
        

        longest = [node_id]
        max_length = 0
        
        for succ in successors:
            path = self._build_longest_path(succ, nodes, edges, visited.copy())
            if len(path) > max_length:
                max_length = len(path)
                longest = [node_id] + path
        
        return longest
    
    def _optimize_for_parallelism(self, dag: Dict, analysis: DAGOptimization) -> Dict:

        nodes = dag["nodes"]
        edges = dag["edges"]
        

        levels = self._compute_execution_levels(nodes, edges)
        

        for node_id, level in levels.items():
            nodes[node_id]["execution_level"] = level
        
        return dag
    
    def _compute_execution_levels(self, nodes: Dict, edges: List) -> Dict:
        levels = {nid: 0 for nid in nodes}
        

        changed = True
        while changed:
            changed = False
            for edge in edges:
                from_node = edge["from"]
                to_node = edge["to"]
                
    
                if levels[to_node] <= levels[from_node]:
                    levels[to_node] = levels[from_node] + 1
                    changed = True
        
        return levels
    
    def _create_execution_plan(self, dag: Dict, components: List) -> Dict:
        plan = {
            "task_id": "task_" + str(hash(str(components)) % 100000),
            "nodes": [],
            "edges": dag["edges"],
            "execution_strategy": "level_by_level",
            "estimated_total_duration_ms": sum(
                node.get("estimated_duration_ms", 100) 
                for node in dag["nodes"].values()
            ),
            "parallelization_metadata": {
                "levels": len(set(
                    node.get("execution_level", 0) 
                    for node in dag["nodes"].values()
                )),
                "expected_speedup": 2.5
            }
        }
        

        for node_id, node in dag["nodes"].items():
            plan["nodes"].append({
                "id": node_id,
                "description": node["description"],
                "complexity": node["complexity"],
                "estimated_duration_ms": node["estimated_duration_ms"],
                "execution_level": node.get("execution_level", 0),
                "type": "task",
                "tool_suggestions": self._suggest_tools(node["description"]),
                "inputs": [],
                "outputs": [f"result_{node_id}"]
            })
        
        return plan
    
    @staticmethod
    def _estimate_complexity(task: str) -> str:
        keywords = {
            "complex": ["architecture", "design", "system"],
            "moderate": ["implement", "test", "document"],
            "simple": ["analyze", "research", "generate"]
        }
        
        task_lower = task.lower()
        
        for level, words in keywords.items():
            if any(word in task_lower for word in words):
                return level
        
        return "moderate"
    
    @staticmethod
    def _estimate_duration(task: str) -> int:
        complexity_map = {
            "analyze": 500,
            "research": 2000,
            "design": 3000,
            "implement": 5000,
            "test": 2000,
            "document": 1500,
            "report": 1000,
            "generate": 800
        }
        
        for keyword, duration in complexity_map.items():
            if keyword in task.lower():
                return duration
        
        return 2000
    
    @staticmethod
    def _suggest_tools(description: str) -> List[str]:
        tool_map = {
            "research": ["browser.search", "data.query"],
            "implement": ["code.run", "file.write"],
            "test": ["code.run", "code.analyze"],
            "analyze": ["data.query", "code.analyze"],
            "design": ["file.write"],
            "document": ["file.write"]
        }
        
        tools = []
        for keyword, tool_list in tool_map.items():
            if keyword in description.lower():
                tools.extend(tool_list)
        
        return list(set(tools)) or ["browser.search"]
