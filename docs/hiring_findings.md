# Hiring Simulator — Key Findings

## Core Question
> Under what conditions do candidates accept job offers, and how does asymmetric information affect hiring efficiency?

## Key Parameters
| Parameter | Value |
|-----------|-------|
| CEO budget | $500,000 |
| HP assessment skill | 85% |
| Candidates | 20 |
| Desperation range | 0.1-0.9 |
| Skill range | 30-95 |

## Emergent Behaviors Observed
1. **Overconfident candidates struggle** (Bob rejected 40+ offers)
2. **Desperate candidates accept lower offers** (Diana at $30k)
3. **Trust collapses with bad hires** (CEO trust dropped to 0.1-0.2)

## What Surprised Me
- The negotiation loop — candidates with medium desperation kept negotiating instead of accepting/rejecting
- Budget exhaustion happened exactly when it should (no overspend after fix)

## What I'd Change
- Add candidate counter-offers
- Add HP learning from bad hires
- Run 1000 simulations for statistical confidence

## One-Sentence Insight
> *Desperation × (expected_salary / offer) predicts acceptance better than salary alone.*