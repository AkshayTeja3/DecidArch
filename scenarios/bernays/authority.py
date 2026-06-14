import random


class Authority:
    def __init__(self, authority_id, name, trust_score=50.0, domain_relevance=0.5,
                 audience_size=100, corruption_risk=0.1):
        self.authority_id = authority_id
        self.name = name
        self.trust_score = trust_score
        self.domain_relevance = domain_relevance
        self.audience_size = audience_size
        self.corruption_risk = corruption_risk

    def endorse(self, message, source, public_sphere):
        """Endorse the source's message to a subset of receivers"""
        # Get all receivers
        all_receivers = public_sphere.receivers

        # Select up to audience_size random receivers
        num_to_reach = min(self.audience_size, len(all_receivers))
        reached = random.sample(all_receivers, num_to_reach)

        # Each reached receiver gets the message
        for receiver in reached:
            receiver.receive_message(source, self)


    def lose_trust(self, amount):
        self.trust_score = max(0, self.trust_score - amount)


    def gain_trust(self, amount):
        self.trust_score = min(100, self.trust_score + amount)