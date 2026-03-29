import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class MemoryRecallEngine:

    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = memory_dir
        self.episodic_file = os.path.join(memory_dir, "episodic_memory.json")
        self.strategy_file = os.path.join(memory_dir, "strategy_memory.json")
        self.recall_log = []

    def find_similar_tasks(self, current_task: str, limit: int = 3) -> List[Dict]:
        if not os.path.exists(self.episodic_file):
            return []
        
        try:
            with open(self.episodic_file, 'r') as f:
                episodic_data = json.load(f)
        except:
            return []
        
        tasks = episodic_data.get("entries", [])
        
        keywords_current = set(current_task.lower().split())
        
        scored_tasks = []
        for task in tasks[:10]:
            task_desc = task.get("task_description", "").lower()
            keywords_task = set(task_desc.split())
            
            overlap = len(keywords_current & keywords_task)
            if overlap > 0:
                scored_tasks.append({
                    "task_id": task.get("task_id"),
                    "description": task.get("task_description"),
                    "score": task.get("score_quality", 0),
                    "duration_ms": task.get("execution_time_ms"),
                    "tools_used": task.get("tools_used", []),
                    "patterns": task.get("patterns_identified", []),
                    "similarity": overlap
                })
        
        scored_tasks.sort(key=lambda x: x["similarity"], reverse=True)
        return scored_tasks[:limit]

    def recall_strategy(self, task_patterns: List[str]) -> Optional[Dict]:
        if not os.path.exists(self.strategy_file):
            return None
        
        try:
            with open(self.strategy_file, 'r') as f:
                strategy_data = json.load(f)
        except:
            return None
        
        strategies = strategy_data.get("entries", [])
        
        for strategy in strategies:
            strategy_patterns = strategy.get("patterns", [])
            overlap = len(set(task_patterns) & set(strategy_patterns))
            if overlap > 0:
                return {
                    "name": strategy.get("strategy_name"),
                    "description": strategy.get("description"),
                    "effectiveness": strategy.get("effectiveness_score", 0),
                    "times_used": strategy.get("times_applied", 0),
                    "recommended_tools": strategy.get("recommended_tools", [])
                }
        
        return None

    def log_recall(self, task: str, similar_tasks: List[Dict], strategy: Optional[Dict]):
        self.recall_log.append({
            "timestamp": datetime.now().isoformat(),
            "current_task": task,
            "similar_past_tasks": len(similar_tasks),
            "strategy_found": strategy is not None
        })

    def print_memory_recall(self, task: str):
        similar = self.find_similar_tasks(task)
        strategy = self.recall_strategy([])
        
        self.log_recall(task, similar, strategy)
        
        print("\n" + "="*80)
        print("🧠 MEMORY RECALL ENGINE")
        print("="*80)
        
        if similar:
            print(f"\n✅ Found {len(similar)} similar past task(s):")
            for i, sim_task in enumerate(similar, 1):
                print(f"\n  {i}. {sim_task['description'][:60]}...")
                print(f"     Task ID: {sim_task['task_id']}")
                print(f"     Quality Score: {sim_task['score']:.2f}/1.0")
                print(f"     Execution Time: {sim_task['duration_ms']}ms")
                print(f"     Tools Used: {', '.join(sim_task['tools_used'][:2])}")
                if sim_task['patterns']:
                    print(f"     Pattern: {sim_task['patterns'][0]}")
        else:
            print("\n📝 No similar past tasks found. This is a new execution pattern.")
        
        print("\n" + "-"*80)
        
        if strategy:
            print(f"\n🎯 RECOMMENDED STRATEGY: {strategy['name']}")
            print(f"   Description: {strategy['description']}")
            print(f"   Historical Effectiveness: {strategy['effectiveness']:.1%}")
            print(f"   Times Successfully Applied: {strategy['times_used']}")
            print(f"   Recommended Tools: {', '.join(strategy['recommended_tools'])}")
            print("\n   → APPLYING PROVEN STRATEGY")
        else:
            print("\n🚀 No proven strategy available. Starting fresh exploration.")
        
        print("\n" + "="*80 + "\n")
        
        return {
            "similar_tasks": similar,
            "strategy": strategy,
            "will_accelerate": len(similar) > 0 or strategy is not None
        }

def show_memory_insights(memory_dir: str = "memory"):
    engine = MemoryRecallEngine(memory_dir)
    print("\n" + "="*80)
    print("📚 SYSTEM MEMORY & LEARNING INSIGHTS")
    print("="*80)
    
    try:
        if os.path.exists(os.path.join(memory_dir, "episodic_memory.json")):
            with open(os.path.join(memory_dir, "episodic_memory.json"), 'r') as f:
                episodic = json.load(f)
                entries = episodic.get("entries", [])
                if entries:
                    print(f"\n📊 Episodic Memory: {len(entries)} past executions")
                    if entries:
                        latest = entries[-1]
                        print(f"   • Latest Task: {latest.get('task_description')[:50]}...")
                        print(f"   • Quality Score: {latest.get('score_quality', 0):.2f}")
    except:
        pass
    
    try:
        if os.path.exists(os.path.join(memory_dir, "strategy_memory.json")):
            with open(os.path.join(memory_dir, "strategy_memory.json"), 'r') as f:
                strategies = json.load(f)
                entries = strategies.get("entries", [])
                if entries:
                    print(f"\n🎓 Strategy Memory: {len(entries)} learned strategies")
                    best = max(entries, key=lambda x: x.get("effectiveness_score", 0))
                    print(f"   • Best Strategy: {best.get('strategy_name')}")
                    print(f"   • Success Rate: {best.get('effectiveness_score', 0):.1%}")
    except:
        pass
    
    print("\n" + "="*80 + "\n")
