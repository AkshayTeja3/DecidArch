from unittest import expectedFailure
import random
from core.base_agent import BaseAgent


class Candidate(BaseAgent):
    def __init__(self, agent_id, name, desperation, actual_skill, perceived_skill,
                 expected_salary, confidence, interview_experience, status,emotional_volatility):
        # 1. Call parent constructor
        super().__init__(agent_id,name,"Candidate")
        # 2. Set qualities dictionary
        # 3. Set initial state (employed=False, weeks_unemployed=0, current_wealth=0)
        self.qualities={
            "desperation": desperation,
            "actual_skill": actual_skill,
            "perceived_skill": perceived_skill,
            "expected_salary": expected_salary,
            "confidence": confidence,
            "interview_experience": interview_experience,
            "emotional_volatility": emotional_volatility
        }
        self.state={
            "employed":False,
            "weeks_unemployed":0,
            "current_wealth":0,
            "rejection_count":0,
            "status": status
        }

    def perceive(self, environment):
        # Extract: current_offer, job_requirements, time_left, market_average
        pass

    import random

    def decide(self, perceived_info):
        current_offer = perceived_info.get("current_offer", 0)
        expected = self.qualities.get("expected_salary", 50000)
        desperation = self.qualities.get("desperation", 0.3)
        min_salary = expected * 0.4

        if current_offer < min_salary:
            return "reject"

        # Calculate acceptance probability
        if current_offer >= expected:
            prob = 0.9
        elif desperation > 0.7:
            # At 70% of expected: 80% chance; at 40%: 10% chance
            ratio = current_offer / expected
            prob = min(0.8, max(0.1, desperation * (ratio - 0.3) * 2))
        else:
            ratio = current_offer / expected
            prob = min(0.5, max(0.05, desperation * ratio))

        # Add random noise (±15%)
        prob = prob * random.uniform(0.85, 1.15)
        prob = max(0, min(1, prob))

        r = random.random()
        if r < prob:
            return "accept"
        elif r < prob + 0.15:
            return "negotiate"
        else:
            return "reject"

    def act(self, decision, environment, offer_amount=0):
        if decision == "accept":
            self.state["employed"] = True
            self.state["current_wealth"] += offer_amount
            self.state["weeks_unemployed"] = 0  # Reset unemployment counter
            # Desperation resets on acceptance (handled in update_state)
        elif decision == "negotiate":
            self.state["rejection_count"] += 1
            # weeks_unemployed increments in update_state
        elif decision == "reject":
            self.state["rejection_count"] += 1
            # weeks_unemployed increments in update_state



        # If accept: update state, remove self from candidate pool
        # If negotiate: send counter_offer
        # If decline: increase weeks_unemployed, update desperation
        pass

    def update_state(self, environment):
        # If employed, desperation stays low (no increase)
        if not self.state.get("employed", False):
            self.state["weeks_unemployed"] += 1  # Increment each step unemployed
            self.qualities["desperation"] = self.calculate_desperation()
        else:
            # If employed, keep desperation at base (or slowly decrease over time)
            pass

        # Log to memory
        self.memory.append({
            "step": getattr(environment, "current_step", 0),
            "desperation": self.qualities["desperation"],
            "employed": self.state["employed"],
            "weeks_unemployed": self.state["weeks_unemployed"]
        })



    def calculate_desperation(self):
        # Use CURRENT desperation, not original
        current = self.qualities.get("desperation", 0.3)

        rejections = self.state.get("rejection_count", 0)
        rejection_penalty = max(0, (rejections - 3)) * 0.05

        weeks = self.state.get("weeks_unemployed", 0)
        time_penalty = weeks * 0.02

        actual = self.qualities.get("actual_skill", 50)
        perceived = self.qualities.get("perceived_skill", 50)
        gap_penalty = abs(actual - perceived) / 100 * 0.01

        volatility = self.qualities.get("emotional_volatility",0.1)
        total=current+rejection_penalty+time_penalty+gap_penalty
        noise=random.uniform(-0.15,0.15)
        total=total+noise
        #total=total+random.uniform(-volatility,volatility)


        #total = current + rejection_penalty + time_penalty + gap_penalty
        return max(0, min(1, total))




class HiringProfessional(BaseAgent):
    def __init__(self, agent_id, name, skill_at_assessment, mistake_tolerance,
                 budget_frugality, promotion_drive, risk_aversion):
        super().__init__(agent_id, name, "HiringProfessional")
        self.qualities = {
            "skill_at_assessment": skill_at_assessment,
            "mistake_tolerance": mistake_tolerance,
            "budget_frugality": budget_frugality,
            "promotion_drive": promotion_drive,
            "risk_aversion": risk_aversion,
        }
        self.state = {
            #"remaining_budget": initial_budget,
            "hires_made": 0,
            "bad_hires": 0,
            "offers_made": []
        }

    def assess_candidate(self, candidate):
        true_skill = candidate.qualities["actual_skill"]

        import random
        if random.random() < (self.qualities["skill_at_assessment"] / 100):
            perceived = true_skill
        else:
            error = random.randint(-20, 20)  # ✅ Fixed
            perceived = max(0, min(100, true_skill + error))

        return perceived

    def decide(self, perceived_info):
        candidate = perceived_info.get("candidate")
        perceived_skill = self.assess_candidate(candidate)

        base_offer = perceived_skill * 1000
        #offer = min(base_offer, self.state["remaining_budget"] * 0.5)

        return {
            "decision": "make_offer",
            "offer_amount": int(base_offer),
            "candidate_id": candidate.agent_id  # ✅ Fixed key name
        }

    def act(self, decision, environment):
        if decision.get("decision") == "make_offer":
            self.state["offers_made"].append({
                "candidate_id": decision["candidate_id"],
                "amount": decision["offer_amount"],
                "step": getattr(environment, "current_step", 0)  # ✅ Fixed
            })

    def update_state(self, environment):
        pass


class CEO(BaseAgent):  # ✅ Added inheritance
    def __init__(self, agent_id, name, excess_capital, return_expectation,
                 patience, micromanagement, tech_ambition):
        super().__init__(agent_id, name, "CEO")

        self.qualities = {
            "excess_capital": excess_capital,
            "return_expectation": return_expectation,
            "patience": patience,
            "micromanagement": micromanagement,
            "tech_ambition": tech_ambition
        }

        self.state = {
            "remaining_budget": excess_capital,
            "total_hires": 0,
            "good_hires": 0,
            "hp_trust": 1.0,
            "quarter": 0
        }

    def decide(self, perceived_info):
        """Return decision dict with approval and modified offer if needed"""
        hp_offer = perceived_info.get("hp_offer", 0)

        # Case 1: Micromanager CEO always adjusts
        if self.qualities["micromanagement"] > 0.7:
            modified_offer = int(hp_offer * 0.9)
            return {
                "decision": "approve_modified",
                "offer_amount": modified_offer,
                "original_offer": hp_offer
            }

        # Case 2: Low trust → reduce offer
        if self.state["hp_trust"] <= 0.5:
            modified_offer = int(hp_offer * 0.8)
            return {
                "decision": "approve_modified",
                "offer_amount": modified_offer,
                "original_offer": hp_offer
            }

        # Case 3: High trust → approve as is
        return {
            "decision": "approve",
            "offer_amount": hp_offer
        }

    def act(self, decision, environment):
        """Return approved amount WITHOUT deducting"""
        if decision.get("decision") in ["approve", "approve_modified"]:
            return decision.get("offer_amount", 0)
        return 0

    def update_state(self, environment):
        """Evaluate HP performance"""
        if self.state["total_hires"] == 0:
            return

        # ✅ Fixed: good_hires / total_hires
        success_rate = self.state["good_hires"] / self.state["total_hires"]

        # ✅ Fixed: correct key name
        expected = self.qualities["return_expectation"]

        if success_rate < expected:
            self.state["hp_trust"] -= 0.1
        elif success_rate > expected:
            self.state["hp_trust"] += 0.05

        # Clamp trust between 0 and 1
        self.state["hp_trust"] = max(0, min(1, self.state["hp_trust"]))

        # Log to memory
        self.memory.append({
            "step": getattr(environment, "current_step", 0),
            "hp_trust": self.state["hp_trust"],
            "success_rate": success_rate,
            "total_hires": self.state["total_hires"],
            "good_hires": self.state["good_hires"]
        })






