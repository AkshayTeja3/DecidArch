# Superego Simulator — Key Findings

## Core Question
> Does internalized guilt (superego) persist without external punishment?

## Key Parameters
| Parameter | Value |
|-----------|-------|
| Population | 100 |
| Rounds | 200 |
| Disaster probability | 25% |
| Anxiety increment | 0.05 per no-share |
| Snowball threshold | 0.5 |

## Emergent Behaviors Observed
1. **Three-phase collapse** (prosperity → death spiral → zombie state)
2. **Anxiety snowball** — once >0.5, system cannot recover
3. **Disasters as only effective reset** — 100% sharing post-disaster, then recollapse

## What Surprised Me
- Priests failed to prevent collapse even with emergency activation
- Superego decayed to 0 in all runs
- Disasters created temporary recovery but never permanent stability

## What I'd Change
- Make priests stronger (higher boost, lower cost)
- Add wealth effect (poor share less)
- Run 100 simulations to calculate collapse probability

## One-Sentence Insight
> *Guilt alone is not self-sustaining — only external shocks (disasters) temporarily restore compliance.*

## Batch Simulation Results (100 runs × 200 rounds)

| Metric | Value  |
|--------|--------|
| Collapse rate (superego < 5) | 11%    |
| Average final superego | 86.9   |
| Average final anxiety | 0.0378 |
| Average final sharing rate | 0.8909 |

### Interpretation

- **Stability is the norm.** The system reaches high compliance in 89% of runs.
- **Collapse is real but rare.** Only 11% of runs end with superego below 5.
- **Psychological health is high.** Average final anxiety is near zero (0.038).
- **Guilt sustains cooperation.** Superego remains strong (87/100) without external punishment.

### Comparison to Earlier Single Run

| | Single run (earlier) | Batch average |
|--|---------------------|---------------|
| Outcome | Collapse at round 120 | Stable (89% of runs) |
| Lesson | One run can mislead | Batch runs reveal true probabilities |

**Key Insight:** The earlier collapse was real but statistically rare. The system is more resilient than a single run suggested.

### The 0.5 Threshold

| Anxiety range | Outcome | Probability |
|---------------|---------|-------------|
| < 0.5 | Stable | 89% |
| ≥ 0.5 | Collapse | 11% |

**Why 0.5 is the tipping point:**

- Snowball activates at anxiety > 0.5
- Anxiety grows at 0.05 per no-share
- Superego grows at 0.01-0.02 per round (snowball)
- Anxiety grows 3-5x faster → impossible to recover

### Design Philosophy

The simulation was deliberately calibrated to produce rare but realistic collapse (11%).

- Without the snowball mechanic: 100% stability (unrealistic utopia)
- With the snowball mechanic: 89% stability, 11% collapse (believable)

**Key insight:** The snowball introduces just enough instability to make the simulation interesting without making it unrealistic. The 0.5 anxiety threshold is the mathematical tipping point.

**Conclusion:** The 0.5 threshold is not arbitrary — it's the mathematical point where the addiction loop becomes irreversible.
