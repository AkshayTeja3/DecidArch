# Bernays Propaganda Simulator — Key Findings

## Core Question
> *"Credibility is upstream of content. Same message from different sources produces completely different responses."*

## Key Parameters
| Parameter | Value |
|-----------|-------|
| Receivers | 100 |
| Sources | 3 |
| Authorities | 5 |
| Scandal interval | 5 rounds |
| Truth revelation probability | 5-50% (based on belief × credibility) |
| Exposure damage | 20-40 credibility loss |

## Emergent Behaviors Observed
1. **Credibility oscillates** — Never permanently at 100%, typically 20-80%
2. **Scandals cause lasting damage** — Belief drops after exposures, recovers slowly
3. **Truth revelation temporarily restores** — +5 credibility, but decays over time
4. **Long-term equilibrium** — System settles at 20-40% belief, 20-80% credibility

## Three Time Regimes
| Time scale | Behavior |
|------------|----------|
| Short (50 rounds) | Oscillation, belief 30-50, credibility 40-80 |
| Medium (100 rounds) | Gradual decline, belief 20-30, credibility 20-40 |
| Long (500 rounds) | Collapse possible without reinforcement |

## Key Insight
> *Propaganda works in the short term, but over long time horizons, credibility inevitably decays without constant reinforcement. Truth eventually catches up.*

## Comparison with Bernays' Claims
| Bernays' claim | Simulation shows |
|----------------|------------------|
| Propaganda can shape opinion | ✅ Yes, temporarily |
| Credibility is an asset | ✅ Yes, but can be destroyed |
| Truth eventually catches up | ✅ Yes — scandals accumulate |
| Propaganda machines can collapse | ✅ Yes — long-term erosion is real |

## Design Decisions That Mattered
- Three-layer agent architecture (Source → Authority → Receiver)
- Asymmetric trust updates (lose trust faster than gain)
- Belief decay (2% per round without reinforcement)
- Scandal probability tied to belief × credibility

## What I'd Change
- Add competing sources with opposing messages
- Add receiver memory decay (forgetting past scandals)
- Test different network topologies (small-world vs random)