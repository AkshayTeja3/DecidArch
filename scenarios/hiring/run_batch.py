from core.batch_runner import BatchRunner

if __name__ == "__main__":
    runner = BatchRunner(
        num_runs=100,
        ceo_budget=500000,
        hp_skill=85,
        num_candidates=20
    )
    runner.run_batch()