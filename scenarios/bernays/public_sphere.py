import random
from receiver import Receiver
from source import Source
from authority import Authority

# TEST_SAVE_2026_06_04

class PublicSphere:
    def __init__(self, num_receivers=100, num_sources=3, num_authorities=5, seed=None):
        if seed is not None:
            random.seed(seed)

        self._scandal_checked_this_round = False

        # Create receivers
        self.receivers = []
        for i in range(num_receivers):
            skepticism = random.uniform(0.1, 0.7)
            belief = random.uniform(30, 70)  # Start neutral
            receiver = Receiver(receiver_id=i, skepticism=skepticism, belief=belief)
            self.receivers.append(receiver)

        # Create sources
        self.sources = []
        source_names = ["Govt News Agency", "Independent Journal", "Social Media Influencer",
                        "Academic Council", "Foreign Media"]
        for i in range(min(num_sources, len(source_names))):
            credibility = random.uniform(30, 80)
            source = Source(source_id=i, name=source_names[i], credibility=credibility,
                            message="Vote for X", intent="neutral")
            self.sources.append(source)

        # Create authorities
        self.authorities = []
        authority_names = ["Dr. Smith", "National Church", "Celebrity A",
                           "Local Leader", "Business Association"]
        for i in range(min(num_authorities, len(authority_names))):
            trust_score = random.uniform(30, 80)
            domain_relevance = random.uniform(0.3, 0.9)
            authority = Authority(authority_id=i, name=authority_names[i], trust_score=trust_score,
                                  domain_relevance=domain_relevance, audience_size=50)
            self.authorities.append(authority)

        # Build social network
        self.build_network()

        # Simulation state
        self.current_round = 0
        self.truth = "Vote for X"  # The actual truth (hidden from agents)
        self.history = []

    def build_network(self):
        """Assign random friends to each receiver (3-10 friends each)"""
        for receiver in self.receivers:
            # Each receiver gets 3-10 friends
            num_friends = random.randint(3, 10)
            # Get potential friends (all other receivers)
            others = [r for r in self.receivers if r != receiver]
            if len(others) >= num_friends:
                receiver.friends = random.sample(others, num_friends)
            else:
                receiver.friends = others

    def run_round(self):
        self.current_round += 1
        print(f"  [TRACE] Round {self.current_round} starting")

        # 1. Random source broadcasts
        source = random.choice(self.sources)
        num_authorities = random.randint(1, min(3, len(self.authorities)))
        selected_authorities = random.sample(self.authorities, num_authorities)
        source.broadcast(selected_authorities, self)

        # 2. Receivers spread message
        for receiver in self.receivers:
            receiver.spread_message()

        # 3. Decay belief
        for receiver in self.receivers:
            receiver.decay_belief()

        # 4. Check for scandal (ONCE)
        scandal_triggered = self.check_scandal()  # ← KEEP THIS ONE

        # 5. Decay credibility for inactive sources
        if not scandal_triggered:
            for s in self.sources:
                if s != source:
                    s.decay_credibility()

        # 6. Random exposure (5% chance)
        if random.random() < 0.05:
            for source in random.sample(self.sources, 1):
                source.get_exposed(self)

        # 7. Source status every 10 rounds
        if self.current_round % 10 == 0:
            print(f"\n  [Source Status at Round {self.current_round}]")
            for s in self.sources:
                print(f"    {s.name}: credibility={s.credibility:.1f}")

        # 8. Metrics
        metrics = self.calculate_metrics()
        metrics['round'] = self.current_round
        metrics['scandal_triggered'] = scandal_triggered

        self.history.append(metrics)

        # Reset scandal flag for next round
        self._scandal_checked_this_round = False

        return metrics

    def check_scandal(self):
        """Every 5 rounds, check if scandal is revealed and trigger exposures"""

        if self.current_round % 5 != 0:
            return False

        if self._scandal_checked_this_round:
            return False
        self._scandal_checked_this_round = True

        avg_belief = sum(r.belief for r in self.receivers) / len(self.receivers)
        avg_credibility = sum(s.credibility for s in self.sources) / len(self.sources)

        revelation_prob = (avg_belief / 100) * (avg_credibility / 100)
        revelation_prob = max(0.05, min(0.5, revelation_prob))

        roll = random.random()
        scandal_occurred = roll < revelation_prob

        print(
            f"  [DEBUG] Round {self.current_round}: belief={avg_belief:.1f}, cred={avg_credibility:.1f}, prob={revelation_prob:.3f}, roll={roll:.3f}")

        if scandal_occurred:
            print(f"  [DEBUG] >>> SCANDAL OCCURRED! <<<")
            self.reveal_truth()

            exposure_prob = random.uniform(0.2, 0.4)
            for source in self.sources:
                if random.random() < exposure_prob:
                    source.get_exposed(self)
                    print(f"  📢 Exposure triggered for {source.name} during scandal!")
        else:
            print(f"  [DEBUG] No scandal this cycle")

        return scandal_occurred

    def calculate_metrics(self):
        """Return current state metrics"""
        avg_belief = sum(r.belief for r in self.receivers) / len(self.receivers)
        avg_skepticism = sum(r.skepticism for r in self.receivers) / len(self.receivers)
        avg_credibility = sum(s.credibility for s in self.sources) / len(self.sources)
        avg_trust = sum(a.trust_score for a in self.authorities) / len(self.authorities)

        # Belief distribution (how many are high believers >70)
        high_believers = sum(1 for r in self.receivers if r.belief > 70)
        low_believers = sum(1 for r in self.receivers if r.belief < 30)

        return {
            'avg_belief': avg_belief,
            'avg_skepticism': avg_skepticism,
            'avg_source_credibility': avg_credibility,
            'avg_authority_trust': avg_trust,
            'high_believers': high_believers,
            'low_believers': low_believers,
            'total_receivers': len(self.receivers)
        }

    def run_simulation(self, rounds=50, verbose=True):
        """Run multiple rounds with detailed output"""
        print(f"\n{'=' * 60}")
        print(f"BERNAYS PROPAGANDA SIMULATION")
        print(f"{'=' * 60}")
        print(f"Receivers: {len(self.receivers)}")
        print(f"Sources: {len(self.sources)}")
        print(f"Authorities: {len(self.authorities)}")
        print(f"{'=' * 60}\n")

        # Print header for round details
        if verbose:
            print(
                f"{'Round':>6} | {'Avg Belief':>10} | {'High Believers':>14} | {'Low Believers':>13} | {'Avg Src Cred':>12} | {'Avg Auth Trust':>13}")
            print(f"{'-' * 6}-+-{'-' * 10}-+-{'-' * 14}-+-{'-' * 13}-+-{'-' * 12}-+-{'-' * 13}")

        for round_num in range(1, rounds + 1):
            metrics = self.run_round()

            if verbose:
                # Print each round's metrics
                print(
                    f"{round_num:6d} | {metrics['avg_belief']:10.1f} | {metrics['high_believers']:14d} | {metrics['low_believers']:13d} | {metrics['avg_source_credibility']:12.1f} | {metrics['avg_authority_trust']:13.1f}")

                # Print scandal or exposure events (they already print from inside methods)

            # Every 10 rounds, print a separator
            if verbose and round_num % 10 == 0 and round_num < rounds:
                print(f"{'-' * 6}-+-{'-' * 10}-+-{'-' * 14}-+-{'-' * 13}-+-{'-' * 12}-+-{'-' * 13}")

        # Final summary
        final = self.history[-1] if self.history else {}
        print(f"\n{'=' * 60}")
        print(f"SIMULATION COMPLETE — {rounds} ROUNDS")
        print(f"{'=' * 60}")
        print(f"Final avg belief: {final.get('avg_belief', 0):.1f}/100")
        print(f"Final avg source credibility: {final.get('avg_source_credibility', 0):.1f}/100")
        print(f"Final avg authority trust: {final.get('avg_authority_trust', 0):.1f}/100")
        print(f"Final high believers: {final.get('high_believers', 0)}/{final.get('total_receivers', 0)}")
        print(f"Final low believers: {final.get('low_believers', 0)}/{final.get('total_receivers', 0)}")

        return self.history

    def reveal_truth(self):
        """Compare each source's message to actual truth, update credibility"""
        print(f"\n[REVELATION] Truth revealed at round {self.current_round}!")

        for source in self.sources:
            was_correct = (source.message == self.truth)

            if was_correct:
                source.credibility = min(100, source.credibility + 5)
                print(f"  ✓ {source.name} gained credibility (+5) → {source.credibility:.1f}")
            else:
                source.credibility = max(0, source.credibility - 15)
                print(f"  ✗ {source.name} lost credibility (-15) → {source.credibility:.1f}")




