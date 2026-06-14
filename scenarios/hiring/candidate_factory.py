import random
from hiring.agents import Candidate

def generate_random_candidate(candidate_id, name):
    """Generate a random candidate with realistic distributions"""

    # Skill distribution: normal around 50-70
    actual_skill = random.randint(30, 95)

    # Perceived skill can be off by -20 to +20
    perceived_skill = max(0, min(100, actual_skill + random.randint(-20, 20)))

    # Desperation: higher for lower skill (skilled people less desperate)
    desperation = max(0.1, min(0.9, 1 - (actual_skill / 100) + random.uniform(-0.2, 0.2)))

    # Expected salary: roughly skill × 1000 ± variance
    expected_salary = actual_skill * 1000 + random.randint(-15000, 15000)
    expected_salary = max(30000, min(120000, expected_salary))

    # Confidence: higher when perceived > actual
    confidence = 0.5 + (max(0, perceived_skill - actual_skill) / 100)
    confidence = max(0.1, min(0.9, confidence))

    # Interview experience: random
    interview_exp = random.randint(20, 90)

    emotional_volatility = random.uniform(-0.2, 0.5)

    # Status based on desperation
    if desperation > 0.7:
        status = "desperate_seeker"
    elif desperation < 0.3:
        status = "picky"
    else:
        status = "balanced"

    return Candidate(
        agent_id=candidate_id,
        name=name,
        desperation=desperation,
        actual_skill=actual_skill,
        perceived_skill=perceived_skill,
        expected_salary=expected_salary,
        confidence=confidence,
        interview_experience=interview_exp,
        status=status,
        emotional_volatility=emotional_volatility
    )