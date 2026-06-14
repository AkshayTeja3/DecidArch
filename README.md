# DecidArch — Simulation Framework for Human Behavior Under Constraints

DecidArch is a modular, multi-agent simulation framework for studying human behavior under incentive constraints, guilt dynamics, and propaganda influence.

Built as part of a personal exploration into behavioral economics, Freudian psychology, and Bernaysian propaganda — DecidArch turns theory into runnable experiments.

---

## 📚 Simulations

| Simulation | Core Question | Key Finding |
|------------|---------------|-------------|
| **Hiring** | How does asymmetric information affect hiring? | Desperation × expected salary predicts acceptance better than salary alone |
| **Superego** | Does guilt persist without external punishment? | 11% collapse rate; anxiety > 0.5 is mathematical point of no return |
| **Bernays** | How does borrowed authority change belief adoption? | Credibility oscillates; long-term decay inevitable without reinforcement |

---

## 🏗️ Architecture

```
DecidArch/
├── core/                    # Reusable base classes
│   ├── base_agent.py        # Abstract agent class
│   └── batch_runner.py      # Multi-run experiment runner
│
├── scenarios/               # Concrete simulations
│   ├── hiring/              # Economic decision-making
│   ├── superego/            # Guilt and addiction dynamics
│   └── bernays/             # Propaganda and belief spread
│
├── config/                  # YAML configuration files
├── docs/                    # Findings and documentation
├── analysis/                # Visualization and plotting
└── outputs/                 # CSV results (gitignored)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.14+ |
| Data Processing | Pandas |
| Visualization | Matplotlib, Seaborn |
| Configuration | YAML |
| Storage | CSV / SQLite |

---

## 🔬 Key Insights Discovered

### 1. The 0.5 Anxiety Threshold (Superego)
Once average population anxiety exceeds 0.5, superego collapse is **mathematically certain**. Anxiety grows 3-5x faster than superego can recover.

### 2. 11% Collapse Rate (Superego)
Guilt-based societies are stable 89% of the time. Collapse is real but rare — a calibrated design choice, not a bug.

### 3. Credibility Oscillation (Bernays)
Propaganda works in the short term, but over long time horizons (500+ rounds), credibility decays without constant reinforcement. Truth eventually catches up.

### 4. Desperation-Salary Correlation (Hiring)
Desperation × expected salary predicts acceptance better than salary or skill alone. Internal state drives economic decisions.

---

## 🚀 Running a Simulation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Hiring simulation

```bash
python scenarios/hiring/run_hiring.py
```

### 3. Run Superego batch (100 runs)

```bash
python scenarios/superego/run_batch_superego.py
```

### 4. Run Bernays simulation

```bash
python scenarios/bernays/run_bernays.py
```

### 5. Generate plots

```bash
python analysis/run_with_plots.py
```

---

## 📊 Batch Results Summary

| Simulation | Runs | Collapse Rate | Key Metric |
|------------|------|---------------|------------|
| Hiring | 100 | N/A | Avg hires: 7.5 |
| Superego | 100 | 11% | Avg final superego: 86.9 |
| Bernays (50 rounds) | 100 | N/A | Avg credibility: 72.4 |
| Bernays (500 rounds) | 1 | Credibility → 0 | Long-term collapse observed |

---

## 📖 Documentation

- [Hiring Findings](docs/hiring_findings.md)
- [Superego Findings](docs/superego_findings.md)
- [Bernays Findings](docs/bernays_findings.md)

---

## 📁 Requirements

Create `requirements.txt` with:

```
pandas>=2.0.0
matplotlib>=3.5.0
seaborn>=0.12.0
pyyaml>=6.0
numpy>=1.24.0
```

---

## 👤 Author

**Akshay Teja** — Systems Designer & Developer

- [GitHub](https://github.com/AkshayTeja3)
- [Email](mailto:umaakshay26@gmail.com)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

Built from first principles after reading:
- Freud — *Civilization and Its Discontents*
- Bernays — *Propaganda*
- Chanakya — *Arthashastra* (upcoming simulation)

---


---

## 📄 `LICENSE`

```text
MIT License

Copyright (c) 2026 Akshay Teja

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

## ⭐ If you find this interesting

Star the repository and feel free to experiment with parameters in the YAML configs.


