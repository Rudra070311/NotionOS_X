import time
import random
from abc import abstractmethod
from typing import Dict, Any, Optional, Tuple
from agents.base_agent import BaseAgent, AgentDecision

class CriticAgent(BaseAgent):

    def __init__(self, name: str, dimension: str):
        super().__init__(name=name, role=f"Critic - {dimension}")
        self.dimension = dimension
        self.scores = []

    @abstractmethod
    async def evaluate(self, output: Any, context: Dict[str, Any]) -> Tuple[float, str]:
        pass

    async def execute(self, input_data: Dict[str, Any],
                     context: Optional[Dict[str, Any]] = None) -> AgentDecision:
        start_time = time.time()

        output_to_evaluate = input_data.get("output", "")

        try:
            score, feedback = await self.evaluate(output_to_evaluate, context or {})

            self.scores.append(score)

            decision_data = {
                "dimension": self.dimension,
                "score": score,
                "feedback": feedback,
            }

            reasoning = f"Evaluated output on {self.dimension} dimension. "
            reasoning += f"Score: {score:.2f}/1.0. {feedback}"

            execution_time = time.time() - start_time
            decision = AgentDecision(
                agent_name=self.name,
                decision="EVALUATION_COMPLETE",
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
                decision="EVALUATION_FAILED",
                reasoning=f"Evaluation failed: {str(e)}",
                confidence=0.0,
                execution_time=execution_time,
            )
            self.record_decision(error_decision)
            self.execution_count += 1

            return error_decision

    def get_average_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

class QualityCritic(CriticAgent):

    def __init__(self):
        super().__init__(name="QualityCritic", dimension="Quality")

    async def evaluate(self, output: Any, context: Dict[str, Any]) -> Tuple[float, str]:
        output_str = str(output).lower()

        quality_indicators = 0

        if "success" in output_str:
            quality_indicators += 1
        if "complete" in output_str:
            quality_indicators += 1
        if "error" not in output_str:
            quality_indicators += 1
        if "results" in output_str or "output" in output_str:
            quality_indicators += 1
        if "404" not in output_str and "failed" not in output_str:
            quality_indicators += 1

        base_score = quality_indicators / 5.0
        score = min(1.0, base_score + random.uniform(-0.1, 0.15))

        feedback = f"Output shows {'strong' if score > 0.7 else 'adequate' if score > 0.5 else 'weak'} quality signals."

        return score, feedback

class CreativityCritic(CriticAgent):

    def __init__(self):
        super().__init__(name="CreativityCritic", dimension="Creativity")

    async def evaluate(self, output: Any, context: Dict[str, Any]) -> Tuple[float, str]:
        output_str = str(output)
        output_lower = output_str.lower()

        creativity_indicators = 0

        keywords = ["novel", "innovative", "unique", "creative", "original", "synthesis"]
        for keyword in keywords:
            if keyword in output_lower:
                creativity_indicators += 1

        if len(output_str) > 200:
            creativity_indicators += 1

        base_score = creativity_indicators / 7.0
        score = min(1.0, base_score + random.uniform(-0.05, 0.1))

        feedback = f"Output demonstrates {'high' if score > 0.7 else 'moderate' if score > 0.5 else 'low'} creativity."

        return score, feedback

class PracticalityCritic(CriticAgent):

    def __init__(self):
        super().__init__(name="PracticalityCritic", dimension="Practicality")

    async def evaluate(self, output: Any, context: Dict[str, Any]) -> Tuple[float, str]:
        output_str = str(output).lower()

        practicality_indicators = 0

        if "implement" in output_str or "apply" in output_str:
            practicality_indicators += 1
        if "steps" in output_str or "process" in output_str or "procedure" in output_str:
            practicality_indicators += 1
        if "example" in output_str or "case" in output_str:
            practicality_indicators += 1
        if "real" in output_str or "practical" in output_str or "feasible" in output_str:
            practicality_indicators += 1
        if "resource" not in output_str or "requirement" not in output_str:
            practicality_indicators += 1

        base_score = practicality_indicators / 5.0
        score = min(1.0, base_score + random.uniform(-0.05, 0.15))

        feedback = f"Output demonstrates {'strong' if score > 0.7 else 'moderate' if score > 0.5 else 'limited'} practicality."

        return score, feedback
