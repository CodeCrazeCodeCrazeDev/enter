# AEAN — Autonomous Economic Actor Network

A runnable implementation of the AEAN "unified economic organism" described in
the architecture whitepaper. AEAN is not a suite of tools — it is a single
closed-loop system with a shared knowledge substrate, six engines, a
constitutional safety layer, and a compounding flywheel that reinvests every
dollar of revenue into smarter demand detection.

```
demand detection → narrative creation → visual production →
attention capture → revenue conversion → capital reallocation → (repeat)
```

## Architecture

| Component | Module | Role |
|-----------|--------|------|
| **EKG** — Economic Knowledge Graph | `ekg.py` | Central nervous system; every engine reads/writes it. Typed entities + append-only event log. |
| **PAEAN** — capital allocation | `engines/paean.py` | Thompson-Sampling multi-armed bandit; spawns micro-cells, kills losers, scales winners. |
| **ADE** — demand & narrative | `engines/ade.py` | Fuses multi-source signals into demand; engineers narratives via the LLM adapter. |
| **ARE** — revenue & pricing | `engines/are.py` | Funnel (impressions→clicks→conversions), elasticity-optimal pricing, TAM saturation. |
| **AVIE** — visual intelligence | `engines/avie.py` | Generates + scores creative variants (CTR prediction). |
| **Hive Mind** — coordination | `coordination/hive_mind.py` | Agent Token Economics: bids arbitrate scarce compute per cycle. |
| **Research** — discovery | `coordination/research.py` | Mines the EKG for compounding/decaying arms; tracks the 1–6 autonomy ladder. |
| **Governance** — constitution | `governance.py` | Capital-preservation limits, brand-safety filter, earned-autonomy tiers. |
| **Flywheel** — orchestrator | `flywheel.py` | `Organism` wires it all together and runs the compounding loop. |

The whole organism runs **offline with zero external dependencies or API keys** —
the LLM adapter falls back to a deterministic simulator. Supplying
`OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (or `AEAN_LLM_PROVIDER`) transparently
switches narrative/visual generation to a real provider.

## Quick start

```python
from apodex.aean import Organism

organism = Organism(initial_capital_cents=100_000_00, seed=7)
organism.run(cycles=30)
print(organism.snapshot()["cumulative_roi"])
```

### CLI

```bash
python -m apodex.aean --cycles 30 --seed 7
python -m apodex.aean --cycles 50 --capital 250000 --json
```

### Live dashboard

```bash
pip install fastapi uvicorn
uvicorn apodex.aean.dashboard.app:app --port 8000
# open http://localhost:8000
```

Step the flywheel cycle-by-cycle or auto-run it and watch capital compound,
micro-cells spawn/kill/scale, engine autonomy climb, and the Research engine
surface insights in real time.

## Economics model

Micro-cell ROI is driven by a per-arm **latent quality** (unknown to the
organism — Thompson Sampling must learn it), elasticity-based pricing on
contribution margin, and **market saturation** so no cell compounds past its
addressable market. This yields realistic dynamics: structurally weak arms are
auto-liquidated below the ROI floor while proven arms receive 1.5× capital
injections (capped), and the treasury compounds within believable bounds.

## Tests

```bash
python -m pytest tests/aean -q
```
