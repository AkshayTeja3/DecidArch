import random
import csv
import os
from datetime import datetime


class HiringEnvironment:
    def __init__(self, ceo, hiring_professional, candidates):
        self.ceo = ceo
        self.hp = hiring_professional
        self.candidates = candidates  # List of Candidate objects
        self.current_step = 0
        self.current_quarter = 0
        self.active_candidates = candidates.copy()  # Still searching
        self.employed_candidates = []  # Hired
        self.pending_hires = []  # Hires waiting to be evaluated (hire_step, candidate)
        self.results_log = []
        self.budget_exhausted = False

    def run(self, max_steps=100):
        self.budget_exhausted = False  # Add this in __init__ or here

        for step in range(max_steps):
            self.current_step = step

            # ✅ Stop if budget exhausted from previous step
            if self.budget_exhausted:
                print(f"\n💰 Budget exhausted at step {step}")
                break

            # Stop if no candidates left
            if not self.active_candidates:
                print(f"\n✅ All candidates placed at step {step}")
                break

            self.step()

        self.save_results()
        self.print_summary()


    def step(self):
        """One simulation step"""
        # Update quarter (every 12 steps)
        if self.current_step > 0 and self.current_step % 12 == 0:
            self.current_quarter += 1
            self.evaluate_pending_hires()
            self.ceo.update_state(self)

        # If no active candidates, skip
        if not self.active_candidates:
            return

        # Pick a random candidate from active pool
        candidate = random.choice(self.active_candidates)

        # HP assesses candidate and decides offer
        perceived_info = {"candidate": candidate}
        hp_decision = self.hp.decide(perceived_info)

        # CEO reviews HP's decision
        ceo_perceived = {
            "hp_offer": hp_decision.get("offer_amount", 0),
            "hp_recommendation": hp_decision,
            "candidate": candidate
        }
        ceo_decision = self.ceo.decide(ceo_perceived)

        # Get final offer amount
        final_offer = ceo_decision.get("offer_amount", 0)

        # ✅ BUDGET CHECK: Don't proceed if not enough money
        if final_offer > self.ceo.state["remaining_budget"]:
            print(
                f"Step {self.current_step}: 💰 Insufficient budget (need ${final_offer}, have ${self.ceo.state['remaining_budget']})")
            self.budget_exhausted=True
            return  # End simulation or skip

        # Candidate decides
        candidate_perceived = {"current_offer": final_offer}
        candidate_decision = candidate.decide(candidate_perceived)

        # Execute actions
        self.hp.act(hp_decision, self)
        self.ceo.act(ceo_decision, self)
        candidate.act(candidate_decision, self, offer_amount=final_offer)

        # Process candidate's decision
        if candidate_decision == "accept":

            self.active_candidates.remove(candidate)
            self.employed_candidates.append(candidate)
            self.ceo.state["remaining_budget"] -= final_offer
            self.ceo.state["total_hires"] += 1
            self.pending_hires.append({
                "candidate": candidate,
                "hire_step": self.current_step,
                "offer_amount": final_offer
            })
            print(f"Step {self.current_step}: ✅ HIRED {candidate.name} at ${final_offer}")
        elif candidate_decision == "reject":
            print(f"Step {self.current_step}: ❌ REJECTED {candidate.name} (offer ${final_offer})")
        elif candidate_decision == "negotiate":
            print(f"Step {self.current_step}: 🤝 NEGOTIATE {candidate.name} (offer ${final_offer})")

        # Update agent states
        candidate.update_state(self)
        self.hp.update_state(self)

    def evaluate_pending_hires(self):
        """Every quarter, evaluate if hires are good or bad"""
        for hire in self.pending_hires[:]:  # Copy list to modify during iteration
            steps_since_hire = self.current_step - hire["hire_step"]
            if steps_since_hire >= 12:  # One quarter passed
                candidate = hire["candidate"]
                actual_skill = candidate.qualities["actual_skill"]
                expected_skill = candidate.qualities["perceived_skill"]

                if actual_skill >= expected_skill:
                    self.ceo.state["good_hires"] += 1
                    outcome = "GOOD"
                else:
                    outcome = "BAD"

                print(
                    f"  📊 Quarter {self.current_quarter}: {candidate.name} = {outcome} hire (actual {actual_skill} vs expected {expected_skill})")
                self.pending_hires.remove(hire)


    def save_results(self):
        """Save simulation results to CSV"""
        # Create outputs folder if it doesn't exist
        os.makedirs("outputs", exist_ok=True)

        filename = f"outputs/hiring_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["metric", "value"])
            writer.writerow(["total_candidates", len(self.candidates)])
            writer.writerow(["total_hired", len(self.employed_candidates)])
            writer.writerow(["ceo_remaining_budget", self.ceo.state["remaining_budget"]])
            writer.writerow(["hp_bad_hires", self.hp.state["bad_hires"]])
            writer.writerow(["ceo_good_hires", self.ceo.state["good_hires"]])
            writer.writerow(["ceo_hp_trust", self.ceo.state["hp_trust"]])

        print(f"\n📁 Results saved to {filename}")

    def print_summary(self):
        """Print simulation summary"""
        print("\n" + "=" * 50)
        print("SIMULATION SUMMARY")
        print("=" * 50)
        print(f"Total candidates: {len(self.candidates)}")
        print(f"Total hired: {len(self.employed_candidates)}")
        print(f"CEO remaining budget: ${self.ceo.state['remaining_budget']}")
        print(f"CEO good hires: {self.ceo.state['good_hires']}")
        print(f"CEO trust in HP: {self.ceo.state['hp_trust']:.2f}")
        print(f"HP bad hires: {self.hp.state['bad_hires']}")
        print(f"HP offers made: {len(self.hp.state['offers_made'])}")