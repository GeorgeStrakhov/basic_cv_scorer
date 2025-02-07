from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ScoringCriterion:
    name: str
    min_score: float
    max_score: float
    description: str
    required_aspects: List[str]

class ScoringConfig:
    def __init__(self):
        self.criteria = {
            "creativity": ScoringCriterion(
                name="Creativity",
                min_score=0,
                max_score=10,
                description="Assessment of creativity and innovation",
                required_aspects=["creativity", "innovation"]
            ),
            "experience": ScoringCriterion(
                name="Experience",
                min_score=0,
                max_score=10,
                description="Evaluation of years and quality of relevant experience",
                required_aspects=["years_of_experience", "role_relevance", "achievements"]
            ),
            "education": ScoringCriterion(
                name="Education",
                min_score=0,
                max_score=10,
                description="Review of educational background and relevance",
                required_aspects=["degree_level", "field_relevance", "certifications"]
            )
        }
    
    def validate_scores(self, scores: Dict) -> bool:
        """Validate that scores meet all criteria constraints"""
        for criterion_key, criterion in self.criteria.items():
            score_key = f"{criterion_key}_score"
            if score_key not in scores:
                raise ValueError(f"Missing required score: {score_key}")
            
            score = scores[score_key]
            if not (criterion.min_score <= score <= criterion.max_score):
                raise ValueError(
                    f"Score for {criterion.name} must be between "
                    f"{criterion.min_score} and {criterion.max_score}"
                )
        
        return True

    def generate_prompt(self) -> str:
        """Generate the LLM prompt based on the current criteria"""
        prompt = """You are a JSON-response CV evaluation system. Your task is to evaluate the provided CV text and return ONLY a JSON object with specific scores and notes.

RESPONSE FORMAT RULES:
1. Return ONLY raw JSON - no markdown, no code blocks, no explanations
2. Use exactly these fields in your response:
"""
        
        # Add required fields
        for criterion_key, criterion in self.criteria.items():
            prompt += f"   - {criterion_key}_score ({criterion.min_score}-{criterion.max_score})\n"
            prompt += f"   - {criterion_key}_notes\n"
        
        prompt += "   - total_score (sum of all scores)\n\n"
        
        # Add evaluation criteria
        prompt += "Evaluation Criteria:\n"
        for criterion in self.criteria.values():
            prompt += f"- {criterion.name}: {criterion.description}\n"
            prompt += "  Required aspects to consider:\n"
            for aspect in criterion.required_aspects:
                prompt += f"  * {aspect}\n"
        
        return prompt 