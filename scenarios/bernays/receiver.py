import random


class Receiver:
    def __init__(self, receiver_id, skepticism=0.3, belief=50.0):
        self.id = receiver_id
        self.skepticism = skepticism  # 0-1, higher = more resistant
        self.belief = belief  # 0-100
        self.friends = []  # List of other Receiver objects
        self.credibility_memory = {}  # source_id → running credibility

    def receive_message(self, source, authority):
        """Update belief based on source credibility and authority trust"""
        # Raw credibility from source and authority
        raw_credibility = (source.credibility + authority.trust_score) / 2

        # Apply skepticism (higher skepticism = less impact)
        effective_credibility = raw_credibility * (1 - self.skepticism)

        # Weighted average (50% old, 50% new)
        self.belief = (self.belief + effective_credibility) / 2

        # Clamp between 0-100
        self.belief = max(0, min(100, self.belief))

    def update_trust(self, source, was_correct):
        """Update source credibility based on whether they were correct"""
        if was_correct:
            source.credibility = min(100, source.credibility + 5)
        else:
            source.credibility = max(0, source.credibility - 15)

    def spread_message(self):
        """If believer (>70), influence friends"""
        if self.belief > 70:
            for friend in self.friends:
                # Friend's belief moves 30% toward this receiver's belief
                friend.belief += (self.belief - friend.belief) * 0.3
                friend.belief = max(0, min(100, friend.belief))

    def decay_belief(self):
        """Belief decays 2% per round without reinforcement"""
        self.belief *= 0.98
        self.belief = max(0, min(100, self.belief))

    def vote(self):
        """Probability of voting for X equals belief/100"""
        return random.random() < (self.belief / 100)