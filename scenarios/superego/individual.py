import random

class Individual:
    def __init__(self, id, wealth, superego, anxiety=0.0, belief_about_others=50.0):
        """
        id: unique identifier
        wealth: can be negative (debt)
        superego: 0-100, internalized guilt strength
        anxiety: 0-1, builds up from not sharing
        belief_about_others: 0-100, what % they think others share
        """
        self.id = id
        self.wealth = wealth
        self.superego = superego
        self.anxiety = anxiety
        self.belief_about_others = belief_about_others
        self.sharing_history = []  # list of booleans (True = shared)
        self.observed_sharers = 0
        self.observed_total = 0

    def decide_to_share(self, disaster_occurred):
        if disaster_occurred:
            return True

        if self.superego > self.belief_about_others:
            return True
        else:
            return False

    def apply_guilt_penalty(self, shared):
        if not shared:
            self.anxiety += 0.05
            self.anxiety = min(1.0, self.anxiety)

            if self.anxiety > 0.5:
                snowball = self.superego * self.anxiety
                penalty = snowball / 1000
                self.superego += penalty
                self.superego = min(100, self.superego)
        else:
            # ✅ Sharing reduces anxiety and slightly reduces superego
            self.anxiety = max(0, self.anxiety - 0.03)
            self.superego = max(0, self.superego - 0.5)

    def update_belief(self, observed_shares, total_observed):
        if total_observed == 0:
            return

        observed_rate = (observed_shares / total_observed) * 100

        # Update belief
        self.belief_about_others = self.belief_about_others * 0.7 + observed_rate * 0.3
        self.belief_about_others = max(0, min(100, self.belief_about_others))

        # ✅ Also update superego based on social pressure
        # If most others share, superego increases
        social_pressure = (observed_rate - 50) / 50  # -1 to +1 range
        self.superego += social_pressure * 2  # Small adjustment
        self.superego = max(0, min(100, self.superego))