import random
import csv
import os
from society import Society


def run_batch(num_runs=100, rounds=200):
    os.makedirs("outputs",exist_ok=True)
    results = []
    for run_id in range(num_runs):
        # Each run gets a different seed (run_id + base_seed)
        society = Society(seed=run_id + 42)

        for _ in range(rounds):
            metrics = society.run_round()

        # Record final state
        results.append({
            'run_id': run_id,
            'final_sharing_rate': metrics['sharing_rate'],
            'final_superego': metrics['avg_superego'],
            'final_anxiety': metrics['avg_anxiety'],
            'final_temple_wealth': metrics['temple_wealth']
        })

        if run_id % 10 == 0:
            print(f"Completed {run_id}/{num_runs} runs")

    # Save to CSV
    with open('outputs/superego_batch_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # Print summary
    avg_collapse = sum(1 for r in results if r['final_superego'] < 5) / num_runs * 100
    print(f"\n=== Summary ===")
    print(f"Runs with superego < 5: {avg_collapse:.1f}%")
    print(f"Average final superego: {sum(r['final_superego'] for r in results) / num_runs:.1f}")


if __name__ == "__main__":
    run_batch(num_runs=100,rounds=200)