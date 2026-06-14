import random
import yaml
import os
from individual import Individual


class Society:
    def __init__(self, config_path=None, seed=None):
        # 1. Load config
        if config_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            config_path = os.path.join(project_root, "config", "superego_config.yaml")

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # 2. Set seed
        if seed is None:
            seed = self.config['simulation']['random_seed']
        random.seed(seed)

        # 3. Initialize state variables (MUST be before creating individuals if they need them)
        self.current_round = 0
        self.temple_wealth = 0
        self.disaster_probability = self.config['disaster']['probability']

        # 4. Create individuals
        pop_size = self.config['simulation']['population_size']
        wealth_min = self.config['simulation']['initial_wealth_range']['min']
        wealth_max = self.config['simulation']['initial_wealth_range']['max']
        superego_min = self.config['simulation']['initial_superego_range']['min']
        superego_max = self.config['simulation']['initial_superego_range']['max']

        self.individuals = []
        for i in range(pop_size):
            wealth = random.uniform(wealth_min, wealth_max)
            superego = random.uniform(superego_min, superego_max)
            individual = Individual(id=i, wealth=wealth, superego=superego)
            self.individuals.append(individual)

    def check_disaster(self):
        """Return True if disaster occurs this round."""
        return random.random() < self.disaster_probability

    def redistribute_temple_wealth(self):
        """Called on disaster. Distribute all temple wealth equally to all individuals."""
        if not self.individuals:
            return

        per_person = self.temple_wealth / len(self.individuals)
        for individual in self.individuals:
            individual.wealth += per_person


        print(f"[Round {self.current_round}]  🌊 DISASTER! Temple wealth ${self.temple_wealth:,.0f} redistributed (${per_person:,.0f} each)")
        self.temple_wealth=0

    def run_round(self):
        """Execute one complete round of the simulation."""
        self.current_round += 1

        # 1. Check for disaster
        disaster = self.check_disaster()
        if disaster:
            self.redistribute_temple_wealth()

        # 2. Collect shares
        total_shared = 0
        for individual in self.individuals:
            shared = individual.decide_to_share(disaster)
            individual.sharing_history.append(shared)

            if shared:
                # Individual gives 1% of wealth to temple
                share_amount = max(0, individual.wealth * 0.01)
                individual.wealth -= share_amount
                self.temple_wealth += share_amount
                total_shared += 1

            # Apply guilt penalty if they didn't share
            individual.apply_guilt_penalty(shared)

        # 3. Update beliefs based on observations
        self.update_all_beliefs()

        # 4. PRIEST LOGIC (Integrated)
        temple_wealth = self.temple_wealth
        avg_anxiety = sum(ind.anxiety for ind in self.individuals) / len(self.individuals)
        avg_superego = sum(ind.superego for ind in self.individuals) / len(self.individuals)

        # Decision: Should priests activate?
        activate_priests = False

        # Emergency conditions (high anxiety OR very low superego)
        if avg_anxiety > 0.6:
            activate_priests = True
            print(f"[Round {self.current_round}] 🚨 Emergency: High anxiety ({avg_anxiety:.2f})")
        elif avg_superego < 25:
            activate_priests = True
            print(f"[Round {self.current_round}] 🚨 Emergency: Superego collapsing ({avg_superego:.1f})")
        # Normal activation
        elif temple_wealth > 100 and random.random() < 0.3:
            activate_priests = True
        elif temple_wealth > 200:
            activate_priests = True

        if activate_priests and temple_wealth > 50:  # Need minimum wealth
            # Determine effectiveness
            if temple_wealth < 50:
                reduction = 0.05
                cost_rate = 0.20
                boost_chance = 0.15
                boost_amount = 1.0
                corruption_chance = 0.05
                corruption_amount = 0.05
            elif temple_wealth < 100:
                reduction = 0.08
                cost_rate = 0.18
                boost_chance = 0.18
                boost_amount = 1.2
                corruption_chance = 0.08
                corruption_amount = 0.08
            elif temple_wealth < 150:
                reduction = 0.11
                cost_rate = 0.15
                boost_chance = 0.20
                boost_amount = 1.5
                corruption_chance = 0.12
                corruption_amount = 0.10
            elif temple_wealth < 200:
                reduction = 0.14
                cost_rate = 0.12
                boost_chance = 0.22
                boost_amount = 1.8
                corruption_chance = 0.15
                corruption_amount = 0.12
            else:
                reduction = 0.17
                cost_rate = 0.10
                boost_chance = 0.25
                boost_amount = 2.0
                corruption_chance = 0.20
                corruption_amount = 0.15

            # Apply to all individuals
            for individual in self.individuals:
                individual.anxiety *= (1 - reduction)
                if random.random() < boost_chance:
                    individual.superego = min(100, individual.superego + boost_amount)
                individual.superego = max(0, individual.superego - 0.3)

            # Temple pays cost
            cost = self.temple_wealth * cost_rate
            self.temple_wealth -= cost
            print(f"[Round {self.current_round}] 🙏 Priests activated! (cost: ${cost:.0f})")

            # Corruption (only if temple has enough wealth)
            if random.random() < corruption_chance and self.temple_wealth > 100:
                loss = self.temple_wealth * corruption_amount
                self.temple_wealth -= loss
                print(f"[Round {self.current_round}] 😈 Corruption! Temple lost ${loss:.0f}")
        else:
            # No priests this round — normal decay
            for individual in self.individuals:
                individual.superego = max(0, individual.superego - 0.8)
            print(
                f"[Round {self.current_round}] ⛪ Priests inactive (temple wealth: ${temple_wealth:.0f}, anxiety: {avg_anxiety:.2f})")
        metrics = self.calculate_metrics()
        metrics['disaster'] = disaster
        metrics['sharing_count'] = total_shared

        return metrics

    def calculate_metrics(self):
        """Calculate current state metrics."""
        total_wealth = sum(ind.wealth for ind in self.individuals)
        avg_wealth = total_wealth / len(self.individuals)

        total_superego = sum(ind.superego for ind in self.individuals)
        avg_superego = total_superego / len(self.individuals)

        total_anxiety = sum(ind.anxiety for ind in self.individuals)
        avg_anxiety = total_anxiety / len(self.individuals)

        total_belief = sum(ind.belief_about_others for ind in self.individuals)
        avg_belief = total_belief / len(self.individuals)

        sharing_rate = sum(1 for ind in self.individuals
                           if ind.sharing_history and ind.sharing_history[-1]) / len(self.individuals)

        # Simple wealth inequality metric (max/min ratio)
        wealths = [ind.wealth for ind in self.individuals]
        wealth_max = max(wealths)
        wealth_min = min(wealths)
        inequality = wealth_max / (wealth_min + 1) if wealth_min > -1 else wealth_max  # Avoid division by zero

        return {
            'round': self.current_round,
            'temple_wealth': self.temple_wealth,
            'avg_wealth': avg_wealth,
            'avg_superego': avg_superego,
            'avg_anxiety': avg_anxiety,
            'avg_belief': avg_belief,
            'sharing_rate': sharing_rate,
            'inequality': inequality,
            'total_individuals': len(self.individuals)
        }

    def apply_priests(self):
        temple_wealth = self.temple_wealth

        # Determine priest effectiveness based on temple wealth
        if temple_wealth < 50:
            reduction = 0.03
            cost_rate = 0.25
            boost_chance = 0.10
            boost_amount = (0.5, 1.0)
            corruption_chance = 0.05
            corruption_amount = 0.05
        elif temple_wealth < 100:
            reduction = 0.06
            cost_rate = 0.20
            boost_chance = 0.12
            boost_amount = (0.5, 1.0)
            corruption_chance = 0.10
            corruption_amount = 0.08
        elif temple_wealth < 150:
            reduction = 0.09
            cost_rate = 0.15
            boost_chance = 0.13
            boost_amount = (0.7, 1.2)
            corruption_chance = 0.15
            corruption_amount = 0.10
        elif temple_wealth < 200:
            reduction = 0.12
            cost_rate = 0.12
            boost_chance = 0.14
            boost_amount = (0.8, 1.3)
            corruption_chance = 0.20
            corruption_amount = 0.12
        else:
            reduction = 0.15
            cost_rate = 0.08
            boost_chance = 0.15
            boost_amount = (1.0, 1.5)
            corruption_chance = 0.25
            corruption_amount = 0.15

        # Apply to all individuals
        for individual in self.individuals:
            # Anxiety reduction
            individual.anxiety *= (1 - reduction)

            # Superego reinforcement (occasional)
            if random.random() < boost_chance:
                boost = random.uniform(*boost_amount)
                individual.superego = min(100, individual.superego + boost)

            # Baseline superego decay
            individual.superego = max(0, individual.superego - 0.5)

        # Temple pays the cost
        cost = self.temple_wealth * cost_rate
        self.temple_wealth -= cost

        # Corruption
        if random.random() < corruption_chance:
            loss = self.temple_wealth * corruption_amount
            self.temple_wealth -= loss
            print(f"  😈 Corruption! Temple lost ${loss:.0f}")

    def update_all_beliefs(self):
        """Each individual observes a random sample of others and updates beliefs."""
        for individual in self.individuals:
            # Randomly sample 3-10 other individuals
            sample_size = min(random.randint(3, 10), len(self.individuals) - 1)
            if sample_size <= 0:
                continue

            others = [ind for ind in self.individuals if ind != individual]
            sample = random.sample(others, sample_size)

            # Count how many shared in this sample (check last action in history)
            observed_shares = 0
            for ind in sample:
                if ind.sharing_history and ind.sharing_history[-1]:
                    observed_shares += 1

            # Update belief
            individual.update_belief(observed_shares, sample_size)
    