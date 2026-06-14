import pandas as pd
import matplotlib.pyplot as plt


def plot_hiring_simulation(csv_path):
    """Generate all plots from a hiring simulation CSV"""

    # Read the CSV (two columns: metric, value)
    df = pd.read_csv(csv_path)

    # Convert to dictionary for easy access
    data = {}
    for _, row in df.iterrows():
        try:
            data[row['metric']] = float(row['value'])
        except ValueError:
            data[row['metric']] = row['value']

    # Extract values
    total_hired = int(data.get('total_hired', 0))
    total_candidates = int(data.get('total_candidates', 0))
    remaining_budget = float(data.get('ceo_remaining_budget', 0))
    good_hires = int(data.get('ceo_good_hires', 0))
    hp_trust = float(data.get('ceo_hp_trust', 0))
    bad_hires = int(data.get('hp_bad_hires', 0))
    offers_made = int(data.get('hp_offers_made', 0))

    # Calculate derived values
    starting_budget = 500000  # From your simulation
    spent_budget = starting_budget - remaining_budget
    bad_from_trust = total_hired - good_hires  # Bad hires from CEO perspective

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Hiring Simulation Results', fontsize=16, fontweight='bold')

    # Plot 1: Total Hires vs Total Candidates
    axes[0, 0].bar(['Hired', 'Unhired'], [total_hired, total_candidates - total_hired],
                   color=['green', 'gray'])
    axes[0, 0].set_title(f'Placement Rate: {total_hired}/{total_candidates}')
    axes[0, 0].set_ylabel('Count')
    for i, v in enumerate([total_hired, total_candidates - total_hired]):
        axes[0, 0].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

    # Plot 2: Budget Spent vs Remaining
    axes[0, 1].pie([spent_budget, remaining_budget],
                   labels=[f'Spent: ${spent_budget:,.0f}', f'Remaining: ${remaining_budget:,.0f}'],
                   autopct='%1.1f%%',
                   colors=['#ff9999', '#66b3ff'])
    axes[0, 1].set_title(f'Budget Utilization (${starting_budget:,.0f} total)')

    # Plot 3: Good vs Bad Hires
    axes[1, 0].bar(['Good Hires', 'Bad Hires'], [good_hires, bad_from_trust],
                   color=['green', 'red'])
    axes[1, 0].set_title(f'Hire Quality: {good_hires}/{total_hired} good')
    axes[1, 0].set_ylabel('Count')
    for i, v in enumerate([good_hires, bad_from_trust]):
        axes[1, 0].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

    # Plot 4: CEO Trust in HP
    axes[1, 1].bar(['CEO Trust'], [hp_trust], color=['orange'])
    axes[1, 1].set_ylim(0, 1)
    axes[1, 1].set_title(f'CEO Trust in HP: {hp_trust:.2f}')
    axes[1, 1].set_ylabel('Trust Level')
    axes[1, 1].text(0, hp_trust + 0.05, f'{hp_trust:.2f}', ha='center', fontweight='bold')

    # Add offers made as text annotation
    fig.text(0.5, 0.02, f'Total offers made by HP: {offers_made} | '
                        f'Average offers per hire: {offers_made / total_hired:.1f}',
             ha='center', fontsize=10, style='italic')

    plt.tight_layout()
    plt.show()

    # Print summary
    print("\n" + "=" * 50)
    print("PLOT SUMMARY")
    print("=" * 50)
    print(f"Total candidates: {total_candidates}")
    print(f"Total hired: {total_hired} ({total_hired / total_candidates * 100:.0f}% placement)")
    print(f"Budget spent: ${spent_budget:,.0f} ({spent_budget / starting_budget * 100:.1f}%)")
    print(f"Good hires: {good_hires}/{total_hired} ({good_hires / total_hired * 100:.0f}% success)")
    print(f"CEO trust in HP: {hp_trust:.2f}")
    print(f"Offers made per hire: {offers_made / total_hired:.1f}")


def plot_multiple_runs(csv_files):
    """Compare multiple simulation runs"""
    if not csv_files:
        print("No CSV files provided")
        return

    runs_data = []
    for csv_path in csv_files:
        df = pd.read_csv(csv_path)
        data = {'file': csv_path.split('/')[-1]}
        for _, row in df.iterrows():
            try:
                data[row['metric']] = float(row['value'])
            except:
                pass
        runs_data.append(data)

    df_runs = pd.DataFrame(runs_data)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Multiple Simulation Runs Comparison', fontsize=16)

    # Total hires
    axes[0, 0].bar(range(len(df_runs)), df_runs['total_hired'])
    axes[0, 0].set_title('Total Hires')
    axes[0, 0].set_xticks(range(len(df_runs)))
    axes[0, 0].set_xticklabels([f'Run {i + 1}' for i in range(len(df_runs))])

    # Good hires
    axes[0, 1].bar(range(len(df_runs)), df_runs['ceo_good_hires'], color='green')
    axes[0, 1].set_title('Good Hires')
    axes[0, 1].set_xticks(range(len(df_runs)))
    axes[0, 1].set_xticklabels([f'Run {i + 1}' for i in range(len(df_runs))])

    # Trust
    axes[1, 0].bar(range(len(df_runs)), df_runs['ceo_hp_trust'], color='orange')
    axes[1, 0].set_title('CEO Trust in HP')
    axes[1, 0].set_ylim(0, 1)
    axes[1, 0].set_xticks(range(len(df_runs)))
    axes[1, 0].set_xticklabels([f'Run {i + 1}' for i in range(len(df_runs))])

    # Budget remaining
    axes[1, 1].bar(range(len(df_runs)), df_runs['ceo_remaining_budget'], color='blue')
    axes[1, 1].set_title('Remaining Budget ($)')
    axes[1, 1].set_xticks(range(len(df_runs)))
    axes[1, 1].set_xticklabels([f'Run {i + 1}' for i in range(len(df_runs))])

    plt.tight_layout()
    plt.show()