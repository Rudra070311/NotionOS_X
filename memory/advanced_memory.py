import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class EpisodicMemoryEntry:
    task_id: str
    task_description: str
    execution_id: str
    timestamp: str
    dag_nodes: int
    dag_edges: int
    execution_time_ms: int
    success: bool
    output_summary: str
    score_quality: float
    score_creativity: float
    score_practicality: float
    tools_used: List[str]
    patterns_identified: List[str]


@dataclass
class FeedbackMemoryEntry:
    execution_id: str
    failure_point: Optional[str]
    lesson: str
    pattern: str
    fix_applied: str
    effectiveness_score: float
    timestamp: str


@dataclass
class StrategyMemoryEntry:
    pattern_name: str
    pattern_description: str
    applicable_contexts: List[str]
    success_rate: float
    average_improvement: float
    tool_recommendations: Dict[str, float]  # tool_name -> effectiveness


class AdvancedMemorySystem:
    
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = memory_dir
        os.makedirs(f"{memory_dir}/episodic", exist_ok=True)
        os.makedirs(f"{memory_dir}/feedback", exist_ok=True)
        os.makedirs(f"{memory_dir}/strategy", exist_ok=True)
        
        self.episodic_memory: Dict[str, EpisodicMemoryEntry] = {}
        self.feedback_memory: List[FeedbackMemoryEntry] = []
        self.strategy_memory: Dict[str, StrategyMemoryEntry] = {}
        
        self._load_all_memories()
        logger.info("🧠 [Memory] Advanced memory system initialized")
    
    # ==================== EPISODIC MEMORY ====================
    
    def store_execution(self, execution_data: Dict) -> str:
        execution_id = execution_data.get("execution_id", f"exec_{hash(str(execution_data)) % 100000}")
        
        entry = EpisodicMemoryEntry(
            task_id=execution_data.get("task_id", "unknown"),
            task_description=execution_data.get("task_description", ""),
            execution_id=execution_id,
            timestamp=datetime.now().isoformat(),
            dag_nodes=len(execution_data.get("dag", {}).get("nodes", {})),
            dag_edges=len(execution_data.get("dag", {}).get("edges", [])),
            execution_time_ms=execution_data.get("execution_time_ms", 0),
            success=execution_data.get("success", False),
            output_summary=execution_data.get("output_summary", "")[:200],
            score_quality=execution_data.get("scores", {}).get("quality", 0.0),
            score_creativity=execution_data.get("scores", {}).get("creativity", 0.0),
            score_practicality=execution_data.get("scores", {}).get("practicality", 0.0),
            tools_used=execution_data.get("tools_used", []),
            patterns_identified=execution_data.get("patterns", [])
        )
        
        self.episodic_memory[execution_id] = entry
        self._persist_episodic_entry(entry)
        
        logger.info(f"💾 [Episodic] Stored execution {execution_id}")
        
        return execution_id
    
    def retrieve_similar_executions(self, query_task: str, limit: int = 5) -> List[Dict]:
        logger.info(f"🔍 [Episodic] Searching for similar executions...")
        
        similar = []
        query_lower = query_task.lower()
        
        for entry in self.episodic_memory.values():
    
            if any(word in entry.task_description.lower() 
                  for word in query_lower.split()):
                similar.append({
                    "execution_id": entry.execution_id,
                    "task": entry.task_description,
                    "success": entry.success,
                    "time_ms": entry.execution_time_ms,
                    "score_quality": entry.score_quality,
                    "timestamp": entry.timestamp
                })
        

        similar.sort(key=lambda x: x["score_quality"], reverse=True)
        
        return similar[:limit]
    
    def get_execution_statistics(self) -> Dict:
        if not self.episodic_memory:
            return {
                "total_executions": 0,
                "success_rate": 0.0,
                "avg_execution_time_ms": 0,
                "avg_quality_score": 0.0
            }
        
        entries = list(self.episodic_memory.values())
        
        successful = sum(1 for e in entries if e.success)
        total_time = sum(e.execution_time_ms for e in entries)
        avg_quality = sum(e.score_quality for e in entries) / len(entries)
        
        return {
            "total_executions": len(entries),
            "success_rate": successful / len(entries) if entries else 0.0,
            "avg_execution_time_ms": total_time / len(entries) if entries else 0,
            "avg_quality_score": avg_quality,
            "most_used_tools": self._get_most_used_tools(),
            "most_common_patterns": self._get_common_patterns()
        }
    
    # ==================== FEEDBACK MEMORY ====================
    
    def store_feedback(self, execution_id: str, feedback_data: Dict) -> None:
        entry = FeedbackMemoryEntry(
            execution_id=execution_id,
            failure_point=feedback_data.get("failure_point"),
            lesson=feedback_data.get("lesson", ""),
            pattern=feedback_data.get("pattern", ""),
            fix_applied=feedback_data.get("fix_applied", ""),
            effectiveness_score=feedback_data.get("effectiveness_score", 0.0),
            timestamp=datetime.now().isoformat()
        )
        
        self.feedback_memory.append(entry)
        self._persist_feedback_entry(entry)
        
        logger.info(f"📚 [Feedback] Stored lesson: {entry.lesson[:50]}")
    
    def get_improvement_opportunities(self) -> List[Dict]:
        logger.info("🎯 [Feedback] Analyzing improvement opportunities...")
        
        improvements = []
        

        pattern_groups = {}
        for entry in self.feedback_memory:
            if entry.pattern not in pattern_groups:
                pattern_groups[entry.pattern] = []
            pattern_groups[entry.pattern].append(entry)
        

        for pattern, entries in pattern_groups.items():
            avg_effectiveness = sum(e.effectiveness_score for e in entries) / len(entries)
            
            if avg_effectiveness < 0.7:  # Low effectiveness threshold
                improvements.append({
                    "pattern": pattern,
                    "occurrences": len(entries),
                    "avg_effectiveness": avg_effectiveness,
                    "lessons": [e.lesson for e in entries],
                    "priority": "HIGH" if avg_effectiveness < 0.5 else "MEDIUM"
                })
        
        return sorted(improvements, key=lambda x: x["avg_effectiveness"])
    
    def extract_lessons(self, topic: str = None) -> List[str]:
        lessons = [e.lesson for e in self.feedback_memory]
        
        if topic:
            topic_lower = topic.lower()
            lessons = [l for l in lessons if topic_lower in l.lower()]
        
        return lessons
    
    # ==================== STRATEGY MEMORY ====================
    
    def store_strategy(self, strategy_data: Dict) -> None:
        entry = StrategyMemoryEntry(
            pattern_name=strategy_data.get("pattern_name", ""),
            pattern_description=strategy_data.get("description", ""),
            applicable_contexts=strategy_data.get("contexts", []),
            success_rate=strategy_data.get("success_rate", 0.0),
            average_improvement=strategy_data.get("improvement", 0.0),
            tool_recommendations=strategy_data.get("tool_recommendations", {})
        )
        
        self.strategy_memory[entry.pattern_name] = entry
        self._persist_strategy_entry(entry)
        
        logger.info(f"🎓 [Strategy] Stored strategy: {entry.pattern_name}")
    
    def recommend_strategy(self, task_description: str) -> Optional[Dict]:
        logger.info("💡 [Strategy] Generating strategy recommendation...")
        
        best_match = None
        best_score = 0.0
        
        task_lower = task_description.lower()
        
        for strategy in self.strategy_memory.values():
    
            match_score = sum(
                1 for context in strategy.applicable_contexts
                if context.lower() in task_lower
            ) / (len(strategy.applicable_contexts) + 1)
            
    
            match_score *= strategy.success_rate
            
            if match_score > best_score:
                best_score = match_score
                best_match = strategy
        
        if best_match:
            return {
                "pattern_name": best_match.pattern_name,
                "description": best_match.pattern_description,
                "tool_recommendations": best_match.tool_recommendations,
                "confidence": best_score
            }
        
        return None
    
    def get_strategy_effectiveness(self) -> Dict:
        if not self.strategy_memory:
            return {}
        
        return {
            strategy_name: {
                "success_rate": strategy.success_rate,
                "average_improvement": strategy.average_improvement,
                "contexts": strategy.applicable_contexts
            }
            for strategy_name, strategy in self.strategy_memory.items()
        }
    
    # ==================== PERSISTENCE ====================
    
    def _persist_episodic_entry(self, entry: EpisodicMemoryEntry) -> None:
        filepath = f"{self.memory_dir}/episodic/{entry.execution_id}.json"
        
        with open(filepath, 'w') as f:
            json.dump(asdict(entry), f, indent=2)
    
    def _persist_feedback_entry(self, entry: FeedbackMemoryEntry) -> None:
        filepath = f"{self.memory_dir}/feedback/{entry.execution_id}.json"
        
        with open(filepath, 'w') as f:
            json.dump(asdict(entry), f, indent=2)
    
    def _persist_strategy_entry(self, entry: StrategyMemoryEntry) -> None:
        filepath = f"{self.memory_dir}/strategy/{entry.pattern_name}.json"
        
        with open(filepath, 'w') as f:
            json.dump(asdict(entry), f, indent=2)
    
    def _load_all_memories(self) -> None:

        episodic_dir = f"{self.memory_dir}/episodic"
        if os.path.exists(episodic_dir):
            for filename in os.listdir(episodic_dir):
                if filename.endswith('.json'):
                    try:
                        with open(f"{episodic_dir}/{filename}") as f:
                            data = json.load(f)
                            entry = EpisodicMemoryEntry(**data)
                            self.episodic_memory[entry.execution_id] = entry
                    except Exception as e:
                        logger.warning(f"Failed to load episodic memory: {e}")
        

        feedback_dir = f"{self.memory_dir}/feedback"
        if os.path.exists(feedback_dir):
            for filename in os.listdir(feedback_dir):
                if filename.endswith('.json'):
                    try:
                        with open(f"{feedback_dir}/{filename}") as f:
                            data = json.load(f)
                            entry = FeedbackMemoryEntry(**data)
                            self.feedback_memory.append(entry)
                    except Exception as e:
                        logger.warning(f"Failed to load feedback memory: {e}")
        

        strategy_dir = f"{self.memory_dir}/strategy"
        if os.path.exists(strategy_dir):
            for filename in os.listdir(strategy_dir):
                if filename.endswith('.json'):
                    try:
                        with open(f"{strategy_dir}/{filename}") as f:
                            data = json.load(f)
                            entry = StrategyMemoryEntry(**data)
                            self.strategy_memory[entry.pattern_name] = entry
                    except Exception as e:
                        logger.warning(f"Failed to load strategy memory: {e}")
    
    def export_memory_snapshot(self) -> Dict:
        return {
            "timestamp": datetime.now().isoformat(),
            "episodic_count": len(self.episodic_memory),
            "feedback_count": len(self.feedback_memory),
            "strategy_count": len(self.strategy_memory),
            "statistics": self.get_execution_statistics(),
            "improvements": self.get_improvement_opportunities(),
            "strategies": self.get_strategy_effectiveness()
        }
    
    # ==================== UTILITY ====================
    
    def _get_most_used_tools(self) -> List[str]:
        tool_counts = {}
        
        for entry in self.episodic_memory.values():
            for tool in entry.tools_used:
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        return sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _get_common_patterns(self) -> List[str]:
        pattern_counts = {}
        
        for entry in self.episodic_memory.values():
            for pattern in entry.patterns_identified:
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        return [p for p, _ in sorted(pattern_counts.items(), 
                                    key=lambda x: x[1], reverse=True)][:5]
