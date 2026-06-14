from scenarios.hiring.agents import Candidate, HiringProfessional, CEO
from scenarios.hiring.environment import HiringEnvironment
from analysis.plots import plot_hiring_simulation, plot_multiple_runs
import glob

# Create agents (same as before)
ceo = CEO("CEO_001", "Jeff", excess_capital=500000,
          return_expectation=0.6, patience=0.7,
          micromanagement=0.3, tech_ambition=0.8)

hp = HiringProfessional("HP_001", "Sarah", skill_at_assessment=85,
                        mistake_tolerance=0.2, budget_frugality=0.5,
                        promotion_drive=0.7, risk_aversion=0.4)

candidates = [
    Candidate("C_001", "Alice", desperation=0.9, actual_skill=85, perceived_skill=80,
              expected_salary=60000, confidence=0.7, interview_experience=70, status="desperate"),
    Candidate("C_002", "Bob", desperation=0.2, actual_skill=45, perceived_skill=70,
              expected_salary=80000, confidence=0.9, interview_experience=50, status="picky"),
    Candidate("C_003", "Charlie", desperation=0.5, actual_skill=90, perceived_skill=85,
              expected_salary=90000, confidence=0.8, interview_experience=85, status="skilled"),
    Candidate("C_004", "Diana", desperation=0.8, actual_skill=30, perceived_skill=40,
              expected_salary=40000, confidence=0.4, interview_experience=30, status="desperate"),
    Candidate("C_005", "Eve", desperation=0.3, actual_skill=75, perceived_skill=75,
              expected_salary=85000, confidence=0.6, interview_experience=65, status="skilled"),
    Candidate("C_006", "Frank", desperation=0.6, actual_skill=60, perceived_skill=60,
              expected_salary=65000, confidence=0.5, interview_experience=55, status="balanced"),
]

# Run simulation
env = HiringEnvironment(ceo, hp, candidates)
env.run(max_steps=100)

# Find the latest CSV file
import glob
import os
csv_files = glob.glob("outputs/hiring_run_*.csv")
if csv_files:
    latest_csv = max(csv_files, key=os.path.getctime)
    print(f"\n📊 Generating plots from {latest_csv}")
    plot_hiring_simulation(latest_csv)

# Optional: compare multiple runs
# plot_all_runs()