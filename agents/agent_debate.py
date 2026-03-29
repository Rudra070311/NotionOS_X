import json
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DebatePosition:
    role: str
    stance: str
    reasoning: str
    impact: str

class AgentDebateEngine:

    def __init__(self):
        self.debate_history = []
        self.roles = {
            "CEO": "Strategic vision and ROI focus",
            "Creative Director": "Innovation, novelty, user engagement",
            "Strategist": "Market positioning, competitor analysis",
            "QA Lead": "Quality, safety, correctness",
            "Tech Lead": "Feasibility, scalability, performance"
        }

    def stage_debate(self, task: str, initial_idea: str, context: Dict = None) -> List[DebatePosition]:
        debate = []
        
        debate.append(DebatePosition(
            role="CEO",
            stance="APPROVED",
            reasoning=f"Strategic alignment confirmed. Task: {task[:50]}... aligns with OKRs.",
            impact="Move forward with execution plan"
        ))
        
        debate.append(DebatePosition(
            role="Creative Director",
            stance="CHALLENGED",
            reasoning=f"Idea too vanilla. Current approach: '{initial_idea[:40]}...' lacks differentiation.",
            impact="Suggest exploring bold creative angles"
        ))
        
        debate.append(DebatePosition(
            role="Strategist",
            stance="REFINED",
            reasoning="Market insights suggest Gen-Z audience prefers authentic, narrative-driven content.",
            impact="Pivot messaging to storytelling format"
        ))
        
        debate.append(DebatePosition(
            role="QA Lead",
            stance="FLAGGED",
            reasoning="Feasibility check: Current approach has 3 potential failure points in execution.",
            impact="Add mitigation strategies before proceeding"
        ))
        
        debate.append(DebatePosition(
            role="Tech Lead",
            stance="OPTIMIZED",
            reasoning="Parallel execution of research and design phases reduces timeline 40%.",
            impact="DAG refactored for optimal resource utilization"
        ))
        
        debate.append(DebatePosition(
            role="CEO",
            stance="FINAL_APPROVED",
            reasoning="All stakeholder concerns addressed. Go-ahead for execution.",
            impact="Lock in sprint commitment"
        ))
        
        self.debate_history.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "positions": [json.loads(json.dumps({
                "role": p.role,
                "stance": p.stance,
                "reasoning": p.reasoning,
                "impact": p.impact
            })) for p in debate]
        })
        
        return debate

    def print_debate(self, debate: List[DebatePosition]):
        print("\n" + "="*80)
        print("🎯 AGENT DEBATE SESSION")
        print("="*80)
        
        for i, position in enumerate(debate, 1):
            emoji_map = {
                "APPROVED": "✅",
                "CHALLENGED": "⚡",
                "REFINED": "🔄",
                "FLAGGED": "⚠️",
                "OPTIMIZED": "🚀",
                "FINAL_APPROVED": "🎯"
            }
            emoji = emoji_map.get(position.stance, "💬")
            
            print(f"\n{i}. {emoji} [{position.role.upper()}] ({position.stance})")
            print(f"   └─ {position.reasoning}")
            print(f"   ➜ Impact: {position.impact}")
        
        print("\n" + "="*80 + "\n")

    def get_consensus(self, debate: List[DebatePosition]) -> Dict:
        return {
            "total_voices": len(debate),
            "final_decision": debate[-1].stance,
            "key_themes": [p.impact for p in debate],
            "ready_to_execute": debate[-1].stance == "FINAL_APPROVED"
        }
