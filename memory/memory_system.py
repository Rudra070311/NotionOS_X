import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

class MemoryStore:

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r') as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
                self.data = {}
        else:
            self.data = {}

    def save(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def add(self, key: str, value: Any):
        self.data[key] = value
        self.save()

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def delete(self, key: str):
        if key in self.data:
            del self.data[key]
            self.save()

    def clear(self):
        self.data = {}
        self.save()

class EpisodicMemory(MemoryStore):

    def __init__(self, filepath: str = "memory/episodic_memory.json"):
        super().__init__(filepath)
        if "tasks" not in self.data:
            self.data["tasks"] = []

    def record_task(self, task_id: str, task_description: str,
                   output: Any, status: str, duration: float):
        task_record = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "description": task_description,
            "output": output,
            "status": status,
            "duration": duration,
        }
        self.data["tasks"].append(task_record)
        self.save()

    def get_task_history(self, limit: int = 10) -> List[Dict]:
        return self.data["tasks"][-limit:]

    def search_tasks(self, keyword: str) -> List[Dict]:
        results = []
        for task in self.data["tasks"]:
            if keyword.lower() in task["description"].lower():
                results.append(task)
        return results

class FeedbackMemory(MemoryStore):

    def __init__(self, filepath: str = "memory/feedback_memory.json"):
        super().__init__(filepath)
        if "feedback_entries" not in self.data:
            self.data["feedback_entries"] = []
        if "improvements" not in self.data:
            self.data["improvements"] = []

    def record_feedback(self, task_id: str, critic: str,
                       score: float, feedback: str, dimension: str = "quality"):
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "critic": critic,
            "dimension": dimension,
            "score": score,
            "feedback": feedback,
        }
        self.data["feedback_entries"].append(feedback_entry)
        self.save()

    def record_improvement(self, task_id: str, dimension: str,
                          old_score: float, new_score: float,
                          improvement_strategy: str):
        improvement = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task_id,
            "dimension": dimension,
            "old_score": old_score,
            "new_score": new_score,
            "improvement": improvement_strategy,
        }
        self.data["improvements"].append(improvement)
        self.save()

    def get_average_scores(self, task_id: str) -> Dict[str, float]:
        scores: Dict[str, List[float]] = {}

        for entry in self.data["feedback_entries"]:
            if entry["task_id"] == task_id:
                dimension = entry["dimension"]
                if dimension not in scores:
                    scores[dimension] = []
                scores[dimension].append(entry["score"])

        averages = {
            dim: sum(scores[dim]) / len(scores[dim])
            for dim in scores
        }
        return averages

    def get_improvement_history(self, task_id: str) -> List[Dict]:
        return [imp for imp in self.data["improvements"]
                if imp["task_id"] == task_id]

class StrategyMemory(MemoryStore):

    def __init__(self, filepath: str = "memory/strategy_memory.json"):
        super().__init__(filepath)
        if "strategies" not in self.data:
            self.data["strategies"] = {}
        if "patterns" not in self.data:
            self.data["patterns"] = []

    def store_strategy(self, strategy_name: str, description: str,
                      effectiveness: float, context: Dict[str, Any]):
        self.data["strategies"][strategy_name] = {
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "effectiveness": effectiveness,
            "context": context,
            "uses": 0,
        }
        self.save()

    def record_pattern(self, pattern_name: str, pattern_data: Dict[str, Any],
                      success_rate: float):
        pattern = {
            "timestamp": datetime.now().isoformat(),
            "name": pattern_name,
            "data": pattern_data,
            "success_rate": success_rate,
        }
        self.data["patterns"].append(pattern)
        self.save()

    def get_best_strategies(self, limit: int = 5) -> List[Dict]:
        strategies = list(self.data["strategies"].values())
        strategies.sort(key=lambda x: x.get("effectiveness", 0), reverse=True)
        return strategies[:limit]

    def use_strategy(self, strategy_name: str):
        if strategy_name in self.data["strategies"]:
            self.data["strategies"][strategy_name]["uses"] += 1
            self.save()

class MemorySystem:

    def __init__(self, memory_dir: str = "memory"):
        self.episodic = EpisodicMemory(os.path.join(memory_dir, "episodic_memory.json"))
        self.feedback = FeedbackMemory(os.path.join(memory_dir, "feedback_memory.json"))
        self.strategy = StrategyMemory(os.path.join(memory_dir, "strategy_memory.json"))

    def save_all(self):
        self.episodic.save()
        self.feedback.save()
        self.strategy.save()

    def get_summary(self) -> Dict[str, Any]:
        return {
            "episodic_tasks": len(self.episodic.data.get("tasks", [])),
            "feedback_entries": len(self.feedback.data.get("feedback_entries", [])),
            "improvements": len(self.feedback.data.get("improvements", [])),
            "strategies": len(self.strategy.data.get("strategies", {})),
            "patterns": len(self.strategy.data.get("patterns", [])),
        }
