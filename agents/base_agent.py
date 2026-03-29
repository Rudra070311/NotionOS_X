"""
Base Agent class for NotionOS X.
All agents inherit from this abstract base class.
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentDecision:
    """Represents an agent's decision."""
    agent_name: str
    decision: str
    reasoning: str
    confidence: float
    execution_time: float
    data: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "agent": self.agent_name,
            "decision": self.decision,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "execution_time": self.execution_time,
            "data": self.data,
        }


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str, role: str):
        """Initialize base agent."""
        self.name = name
        self.role = role
        self.decisions: List[AgentDecision] = []
        self.execution_count = 0
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any], 
                     context: Optional[Dict[str, Any]] = None) -> AgentDecision:
        """Execute agent logic. Must be implemented by subclasses."""
        pass
    
    async def think(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Simulate thinking/reasoning process."""
        # In production, would call LLM API
        # For now, simulate based on signal processing
        return self._simulate_reasoning(prompt)
    
    def _simulate_reasoning(self, prompt: str) -> str:
        """Simulate reasoning output."""
        # Echo back with elaboration
        return f"Analyzed: {prompt}. Key points identified. Proceeding with execution."
    
    def record_decision(self, decision: AgentDecision):
        """Record a decision made by this agent."""
        self.decisions.append(decision)
    
    def get_decision_history(self) -> List[Dict]:
        """Get history of decisions."""
        return [d.to_dict() for d in self.decisions]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        return {
            "name": self.name,
            "role": self.role,
            "execution_count": self.execution_count,
            "total_decisions": len(self.decisions),
            "avg_confidence": (
                sum(d.confidence for d in self.decisions) / len(self.decisions)
                if self.decisions else 0
            ),
        }
