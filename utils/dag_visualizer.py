from typing import Dict, List, Tuple

class DAGVisualizer:

    @staticmethod
    def print_dag_tree(dag: Dict) -> str:
        nodes = dag.get("nodes", {})
        edges = dag.get("edges", [])
        
        if not nodes:
            return "Empty DAG"
        
        node_levels = DAGVisualizer._compute_levels(nodes, edges)
        
        output = []
        output.append("\n" + "="*80)
        output.append("📊 EXECUTION DAG (Task Graph)")
        output.append("="*80 + "\n")
        
        for level in range(max(node_levels.values()) + 1):
            nodes_at_level = [nid for nid, lvl in node_levels.items() if lvl == level]
            
            if nodes_at_level:
                if level > 0:
                    output.append("    ↓")
                
                node_strs = []
                for node_id in nodes_at_level:
                    node_data = nodes.get(node_id, {})
                    node_type = node_data.get("type", "unknown")
                    complexity = node_data.get("complexity", "medium")
                    
                    type_emoji = {
                        "plan": "🧠",
                        "research": "🔍",
                        "execute": "⚙️",
                        "evaluate": "✅",
                        "refine": "🔄"
                    }.get(node_type, "•")
                    
                    node_str = f"{type_emoji} {node_id[:20]}"
                    node_strs.append(node_str)
                
                if len(nodes_at_level) > 1:
                    output.append("[" + "] | [".join(node_strs) + "]")
                    output.append("(parallel execution)")
                else:
                    output.append("[" + node_strs[0] + "]")
        
        parallelization = dag.get("parallelization_metadata", {})
        output.append(f"\n📈 DAG Metrics:")
        output.append(f"  • Total Nodes: {len(nodes)}")
        output.append(f"  • Parallelization Levels: {parallelization.get('levels', 0)}")
        output.append(f"  • Parallelism Factor: {parallelization.get('parallelism_factor', 0):.1%}")
        output.append(f"  • Estimated Duration: {dag.get('estimated_total_duration_ms', 0)}ms")
        output.append("="*80 + "\n")
        
        return "\n".join(output)

    @staticmethod
    def print_execution_flow(dag: Dict) -> str:
        nodes = dag.get("nodes", {})
        edges = dag.get("edges", [])
        
        output = []
        output.append("\n" + "="*60)
        output.append("🔀 EXECUTION FLOW")
        output.append("="*60 + "\n")
        
        node_levels = DAGVisualizer._compute_levels(nodes, edges)
        
        step = 1
        for level in range(max(node_levels.values()) + 1):
            nodes_at_level = [nid for nid, lvl in node_levels.items() if lvl == level]
            
            if len(nodes_at_level) > 1:
                output.append(f"Step {step}: {len(nodes_at_level)} PARALLEL TASKS")
                for node_id in nodes_at_level:
                    output.append(f"  ├─ {node_id}")
            else:
                output.append(f"Step {step}: {nodes_at_level[0]}")
            
            step += 1
        
        output.append("\n" + "="*60 + "\n")
        return "\n".join(output)

    @staticmethod
    def _compute_levels(nodes: Dict, edges: List) -> Dict[str, int]:
        levels = {}
        
        for node_id in nodes:
            levels[node_id] = 0
        
        for source, target in edges:
            if source in levels and target in levels:
                levels[target] = max(levels[target], levels[source] + 1)
        
        return levels

def print_beautiful_dag(dag: Dict):
    print(DAGVisualizer.print_dag_tree(dag))
    print(DAGVisualizer.print_execution_flow(dag))
