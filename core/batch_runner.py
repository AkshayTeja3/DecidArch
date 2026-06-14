# core/batch_runner.py

import random
import csv
from datetime import datetime

import numpy as np


class BatchRunner:
    def __init__(self, num_runs=100, ceo_budget=500000, hp_skill=85, num_candidates=10):
        self.num_runs = num_runs
        self.ceo_budget = ceo_budget
        self.hp_skill = hp_skill
        self.num_candidates = num_candidates
        self.results = []

    def create_random_candidates(self):
        """Generate num_candidates random candidates"""

        # Your code here
        pass

    def run_single_simulation(self, run_id):
        from scenarios.hiring.agents import CEO, HiringProfessional
        from scenarios.hiring.environment import HiringEnvironment
        from scenarios.hiring.candidate_factory import generate_random_candidate

        # Create CEO
        ceo = CEO(f"CEO_{run_id}", "Jeff",
                  excess_capital=self.ceo_budget,
                  return_expectation=0.6, patience=0.7,
                  micromanagement=0.3, tech_ambition=0.8)

        # Create HP
        hp = HiringProfessional(f"HP_{run_id}", "Sarah",
                                skill_at_assessment=self.hp_skill,
                                mistake_tolerance=0.2, budget_frugality=0.5,
                                promotion_drive=0.7, risk_aversion=0.4)

        # Create random candidates
        candidates = []
        for i in range(self.num_candidates):
            name = f"Candidate_{i + 1}"
            candidate = generate_random_candidate(f"C_{run_id}_{i}", name)
            candidates.append(candidate)

        # Run simulation
        env = HiringEnvironment(ceo, hp, candidates)
        env.run(max_steps=100)

        # Calculate metrics
        desperations_hired = [c.qualities["desperation"] for c in env.employed_candidates]
        avg_desperation = sum(desperations_hired) / len(desperations_hired) if desperations_hired else 0

        salaries = [h["offer_amount"] for h in env.pending_hires if h.get("offer_amount")]
        avg_salary = sum(salaries) / len(salaries) if salaries else 0

        offers_made = len(hp.state.get("offers_made", []))
        total_hired = len(env.employed_candidates)
        avg_offers_per_hire = offers_made / total_hired if total_hired > 0 else 0

        total_salary_spent = self.ceo_budget - ceo.state.get("remaining_budget", self.ceo_budget)
        if total_salary_spent > 0 and total_hired > 0:
            budget_efficiency = (ceo.state.get("good_hires", 0) / total_hired) * 100
        else:
            budget_efficiency = 0

        # After the simulation, collect pairs
        desperation_values = []
        salary_values = []

        for candidate in env.employed_candidates:
            # Find the offer this candidate accepted
            for hire in env.pending_hires:
                if hire["candidate"] == candidate:
                    desperation_values.append(candidate.qualities["desperation"])
                    salary_values.append(hire["offer_amount"])
                    break

        # Calculate correlation
        if len(desperation_values) >= 2:
            correlation = np.corrcoef(desperation_values, salary_values)[0, 1]
        else:
            correlation = None

        metrics = {
            "run_id": run_id,
            "total_hired": total_hired,
            "good_hires": ceo.state.get("good_hires", 0),
            "final_trust": ceo.state.get("hp_trust", 0),
            "budget_remaining": ceo.state.get("remaining_budget", 0),
            "avg_desperation_hired": avg_desperation,
            "avg_salary": avg_salary,
            "avg_offers_per_hire": avg_offers_per_hire,
            "budget_efficiency": budget_efficiency,
            "desperation_salary_correlation":correlation
        }

        return metrics

    def run_batch(self):
        """Run all simulations and collect results"""
        print(f"Starting batch of {self.num_runs} simulations...")
        print(f"Parameters: Budget=${self.ceo_budget}, HP Skill={self.hp_skill}, Candidates={self.num_candidates}")
        print("-" * 50)

        for run_id in range(1, self.num_runs + 1):
            metrics = self.run_single_simulation(run_id)
            self.results.append(metrics)

            # Progress indicator
            if run_id % 10 == 0:
                print(f"Completed {run_id}/{self.num_runs} runs")

        self.save_results()
        self.print_summary()

    def save_results(self):
        filename = f"outputs/batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(filename, 'w', newline='') as f:
            fieldnames = self.results[0].keys() if self.results else []
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)

        print(f"\n📁 Batch results saved to {filename}")

    def print_summary(self):
        if not self.results:
            print("No results to summarize")
            return

        # Calculate averages
        avg_hired = sum(r["total_hired"] for r in self.results) / len(self.results)
        avg_trust = sum(r["final_trust"] for r in self.results) / len(self.results)
        avg_efficiency = sum(r["budget_efficiency"] for r in self.results) / len(self.results)

        # Filter out None values for correlation (only keep actual numbers)
        valid_correlations = [r["desperation_salary_correlation"] for r in self.results
                              if r.get("desperation_salary_correlation") is not None]

        print("\n" + "=" * 50)
        print("BATCH RUN SUMMARY")
        print("=" * 50)
        print(f"Total runs: {self.num_runs}")
        print(f"Average hires per run: {avg_hired:.1f}")
        print(f"Average final trust: {avg_trust:.2f}")
        print(f"Average budget efficiency: {avg_efficiency:.1f}%")

        if valid_correlations:
            avg_correlation = sum(valid_correlations) / len(valid_correlations)
            print(
                f"Avg desperation-salary correlation: {avg_correlation:.3f} (based on {len(valid_correlations)} runs)")
        else:
            print(f"Avg desperation-salary correlation: N/A (insufficient data — need at least 2 hires per run)")