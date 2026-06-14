# test_individual.py
from individual import Individual

# Create a test individual
person = Individual(id=1, wealth=100, superego=60)

# Test methods
print(f"Initial: superego={person.superego}, anxiety={person.anxiety}, belief={person.belief_about_others}")

# Test decide_to_share
decision = person.decide_to_share(disaster_occurred=False)
print(f"Decision to share: {decision}")

# Test guilt penalty
person.apply_guilt_penalty(shared=False)
print(f"After guilt: superego={person.superego}, anxiety={person.anxiety}")

# Test update_belief
person.update_belief(observed_shares=5, total_observed=10)
print(f"After belief update: belief={person.belief_about_others}")

print("✅ No syntax errors!")


# test_society.py
from society import Society

# Create society with 20 individuals (for quick test)
society = Society(num_individuals=20)

# Run 5 rounds
for _ in range(50):
    metrics = society.run_round()
    print(f"Round {metrics['round']}: Sharing Rate={metrics['sharing_rate']:.2f}, "
          f"Temple Wealth=${metrics['temple_wealth']:.0f}, "
          f"Avg Superego={metrics['avg_superego']:.1f}, "
          f"Avg Anxiety={metrics['avg_anxiety']:.2f}")