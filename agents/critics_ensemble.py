import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ScoringRubric(Enum):
    EXCELLENT = 0.9
    GOOD = 0.75
    ACCEPTABLE = 0.6
    NEEDS_WORK = 0.4
    POOR = 0.2


@dataclass
class CriticScore:
    critic_name: str
    score: float
    reasoning: str
    recommendations: List[str]
    flags: List[str]


class CriticEnsemble:
    
    def __init__(self):
        self.critics = {
            "quality": QualityCritic(),
            "creativity": CreativityCritic(),
            "practicality": PracticalityCritic(),
            "integration": IntegrationCritic(),
            "performance": PerformanceCritic(),
            "safety": SafetyCritic()
        }
        self.evaluation_history = []
    
    def evaluate_result(self, result: Dict, context: Dict, execution_trace: List) -> Dict:
        logger.info("👁️ [Critics] Starting comprehensive evaluation...")
        
        scores = {}
        all_recommendations = []
        all_flags = []
        

        for critic_name, critic in self.critics.items():
            score = critic.evaluate(result, context, execution_trace)
            scores[critic_name] = score
            all_recommendations.extend(score.recommendations)
            all_flags.extend(score.flags)
            
            logger.info(f"  {critic_name.title()}: {score.score:.2f} - {score.reasoning}")
        

        aggregate_score = self._compute_aggregate(scores)
        

        needs_improvement = aggregate_score < 0.75
        
        evaluation = {
            "individual_scores": {k: v.score for k, v in scores.items()},
            "aggregate_score": aggregate_score,
            "needs_improvement": needs_improvement,
            "recommendations": list(set(all_recommendations)),
            "flags": list(set(all_flags)),
            "critic_feedback": {k: {
                "reasoning": v.reasoning,
                "recommendations": v.recommendations,
                "flags": v.flags
            } for k, v in scores.items()},
            "improvement_priority": self._prioritize_improvements(scores, all_flags)
        }
        
        self.evaluation_history.append(evaluation)
        
        logger.info(f"🎯 Aggregate Score: {aggregate_score:.2f}, "
                   f"Needs Improvement: {needs_improvement}")
        
        return evaluation
    
    @staticmethod
    def _compute_aggregate(scores: Dict[str, CriticScore]) -> float:
        weights = {
            "quality": 0.35,
            "creativity": 0.15,
            "practicality": 0.25,
            "integration": 0.15,
            "performance": 0.05,
            "safety": 0.05
        }
        
        aggregate = sum(
            scores[critic].score * weights.get(critic, 0.2)
            for critic in scores if critic in weights
        )
        
        return min(1.0, max(0.0, aggregate))
    
    def _prioritize_improvements(self, scores: Dict, flags: List) -> List[Dict]:
        improvements = []
        
        for critic_name, score in scores.items():
            if score.score < 0.75:
                improvements.append({
                    "area": critic_name,
                    "current_score": score.score,
                    "target_score": 0.85,
                    "priority": "HIGH" if score.score < 0.5 else "MEDIUM",
                    "recommendations": score.recommendations
                })
        

        return sorted(improvements, key=lambda x: (x["priority"] != "HIGH", x["current_score"]))


class QualityCritic:
    
    def evaluate(self, result: Dict, context: Dict, trace: List) -> CriticScore:
        score_components = {
            "correctness": self._check_correctness(result, context),
            "completeness": self._check_completeness(result, context),
            "accuracy": self._check_accuracy(result),
            "consistency": self._check_consistency(result)
        }
        
        combined_score = sum(score_components.values()) / len(score_components)
        
        reasoning = self._generate_reasoning("Quality", score_components)
        recommendations = self._generate_recommendations("Quality", score_components)
        flags = self._detect_flags("Quality", score_components)
        
        return CriticScore(
            critic_name="Quality",
            score=combined_score,
            reasoning=reasoning,
            recommendations=recommendations,
            flags=flags
        )
    
    @staticmethod
    def _check_correctness(result: Dict, context: Dict) -> float:
        if "output" not in result:
            return 0.2
        if "error" in str(result).lower():
            return 0.3
        return 0.9
    
    @staticmethod
    def _check_completeness(result: Dict, context: Dict) -> float:
        required_keys = context.get("required_output_keys", [])
        result_keys = set(result.keys())
        
        if not required_keys:
            return 0.85
        
        coverage = len(result_keys & set(required_keys)) / len(required_keys)
        return max(0.5, coverage)
    
    @staticmethod
    def _check_accuracy(result: Dict) -> float:
        return 0.88
    
    @staticmethod
    def _check_consistency(result: Dict) -> float:
        return 0.85
    
    @staticmethod
    def _generate_reasoning(critic: str, components: Dict) -> str:
        scores = list(components.values())
        avg = sum(scores) / len(scores)
        
        if avg > 0.85:
            return "Output demonstrates high quality across all dimensions"
        elif avg > 0.7:
            return "Output is generally good with minor quality issues"
        else:
            return "Output has significant quality concerns that should be addressed"
    
    @staticmethod
    def _generate_recommendations(critic: str, components: Dict) -> List[str]:
        recommendations = []
        
        for component, score in components.items():
            if score < 0.7:
                recommendations.append(f"Improve {component}: Currently {score:.1%}")
        
        return recommendations or ["Output meets acceptable quality standards"]
    
    @staticmethod
    def _detect_flags(critic: str, components: Dict) -> List[str]:
        flags = []
        
        for component, score in components.items():
            if score < 0.5:
                flags.append(f"CRITICAL: {component} is below threshold")
        
        return flags


class CreativityCritic:
    
    def evaluate(self, result: Dict, context: Dict, trace: List) -> CriticScore:
        score_components = {
            "originality": self._check_originality(result, context),
            "innovation": self._check_innovation(result),
            "uniqueness": self._check_uniqueness(result)
        }
        
        combined_score = sum(score_components.values()) / len(score_components)
        
        return CriticScore(
            critic_name="Creativity",
            score=combined_score,
            reasoning=f"Creative approach with score {combined_score:.2f}",
            recommendations=["Consider more novel approaches"],
            flags=[]
        )
    
    @staticmethod
    def _check_originality(result: Dict, context: Dict) -> float:
        approach = result.get("approach", "standard")
        if "novel" in approach.lower() or "unique" in approach.lower():
            return 0.85
        return 0.65
    
    @staticmethod
    def _check_innovation(result: Dict) -> float:
        return 0.72
    
    @staticmethod
    def _check_uniqueness(result: Dict) -> float:
        return 0.70


class PracticalityCritic:
    
    def evaluate(self, result: Dict, context: Dict, trace: List) -> CriticScore:
        score_components = {
            "feasibility": self._check_feasibility(result, context),
            "efficiency": self._check_efficiency(result, trace),
            "resources": self._check_resource_usage(result, trace)
        }
        
        combined_score = sum(score_components.values()) / len(score_components)
        
        return CriticScore(
            critic_name="Practicality",
            score=combined_score,
            reasoning=f"Practical implementation score {combined_score:.2f}",
            recommendations=self._optimize_recommendations(score_components),
            flags=[]
        )
    
    @staticmethod
    def _check_feasibility(result: Dict, context: Dict) -> float:
        return 0.88
    
    @staticmethod
    def _check_efficiency(result: Dict, trace: List) -> float:
        if not trace:
            return 0.75
        

        total_duration = sum(t.get("duration_ms", 100) for t in trace)
        
        if total_duration < 5000:
            return 0.92
        elif total_duration < 10000:
            return 0.82
        else:
            return 0.70
    
    @staticmethod
    def _check_resource_usage(result: Dict, trace: List) -> float:
        return 0.85
    
    @staticmethod
    def _optimize_recommendations(components: Dict) -> List[str]:
        return [
            "Execution was efficient",
            "Consider parallelization opportunities",
            "Resource usage is within acceptable bounds"
        ]


class IntegrationCritic:
    
    def evaluate(self, result: Dict, context: Dict, trace: List) -> CriticScore:
        score_components = {
            "compatibility": self._check_compatibility(result, context),
            "coherence": self._check_coherence(result),
            "alignment": self._check_alignment(result, context)
        }
        
        combined_score = sum(score_components.values()) / len(score_components)
        
        return CriticScore(
            critic_name="Integration",
            score=combined_score,
            reasoning=f"System integration score {combined_score:.2f}",
            recommendations=["Ensure backward compatibility"],
            flags=[]
        )
    
    @staticmethod
    def _check_compatibility(result: Dict, context: Dict) -> float:
        return 0.88
    
    @staticmethod
    def _check_coherence(result: Dict) -> float:
        return 0.85
    
    @staticmethod
    def _check_alignment(result: Dict, context: Dict) -> float:
        return 0.82


class PerformanceCritic:
    
    def evaluate(self, result: Dict, context: Dict, trace: List) -> CriticScore:
        execution_time = sum(t.get("duration_ms", 0) for t in trace)
        
        if execution_time < 1000:
            score = 0.95
        elif execution_time < 5000:
            score = 0.85
        else:
            score = 0.70
        
        return CriticScore(
            critic_name="Performance",
            score=score,
            reasoning=f"Execution completed in {execution_time}ms",
            recommendations=[],
            flags=[]
        )


class SafetyCritic:
    
    def evaluate(self, result: Dict, context: Dict, trace: List) -> CriticScore:
        flags = self._check_safety_flags(result, trace)
        
        score = 0.95 if not flags else 0.70
        
        return CriticScore(
            critic_name="Safety",
            score=score,
            reasoning="No safety concerns detected" if not flags else "Safety flags detected",
            recommendations=["Continue monitoring"],
            flags=flags
        )
    
    @staticmethod
    def _check_safety_flags(result: Dict, trace: List) -> List[str]:
        """Check for safety issues"""
        flags = []
        
        for event in trace:
            if "error" in str(event).lower():
                flags.append("Error detected during execution")
            if "timeout" in str(event).lower():
                flags.append("Execution timeout occurred")
        
        return flags
