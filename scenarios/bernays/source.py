import random
import traceback

class Source:
    def __init__(self, source_id, name, credibility=50.0, domain="general", message="Vote for X", intent="neutral"):
        self.source_id = source_id
        self.name = name
        self.credibility = credibility
        self.domain = domain
        self.message = message
        self.intent = intent
        self.exposure_count = 0

    def broadcast(self, authorities, public_sphere):
        for authority in authorities:
            authority.endorse(self.message, self, public_sphere)

    def get_exposed(self, public_sphere, exposure_probability=0.08):  # Add public_sphere parameter
        if random.random() < exposure_probability:
            old_cred = self.credibility
            loss = random.uniform(20, 40)
            self.credibility = max(0, self.credibility - loss)

            # Reduce belief of receivers who might have followed this source
            for receiver in public_sphere.receivers:
                # Simple model: all receivers lose some belief when source exposed
                receiver.belief *= 0.9  # 10% belief drop
                receiver.belief = max(0, min(100, receiver.belief))

            print(f"[EXPOSED] {self.name}: {old_cred:.1f} → {self.credibility:.1f} (lost {loss:.1f})")
            return True
        return False

    def decay_credibility(self):
        # Stronger decay for high credibility
        if self.credibility > 80:
            self.credibility *= 0.97  # 3% decay (was 1%)
        elif self.credibility > 60:
            self.credibility *= 0.98  # 2% decay
        else:
            self.credibility *= 0.99  # 1% decay

    import traceback

    def update_credibility(self, change):
        # Debug: print who called this
        caller = traceback.extract_stack()[-2].name
        print(f"    [DEBUG] {self.name} update_credibility({change}) called from {caller}")

        # Diminishing returns above 70
        if self.credibility > 70 and change > 0:
            change *= 0.3  # 30% effect above 70
        elif self.credibility > 50 and change > 0:
            change *= 0.6  # 60% effect above 50

        self.credibility = max(0, min(100, self.credibility + change))