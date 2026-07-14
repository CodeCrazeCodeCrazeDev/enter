"""Command-line runner for the AEAN organism.

Examples::

    python -m apodex.aean --cycles 30 --seed 7
    python -m apodex.aean --cycles 50 --capital 250000 --json
"""
from __future__ import annotations

import argparse
import json

from .flywheel import Organism


def _fmt_money(cents: int) -> str:
    return f"${cents / 100:,.2f}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AEAN compounding-flywheel simulation.")
    parser.add_argument("--cycles", type=int, default=30, help="Number of flywheel cycles to run.")
    parser.add_argument("--capital", type=float, default=100_000.0, help="Initial treasury capital in dollars.")
    parser.add_argument("--seed", type=int, default=None, help="Deterministic RNG seed.")
    parser.add_argument("--json", action="store_true", help="Emit the final snapshot as JSON.")
    args = parser.parse_args()

    organism = Organism(initial_capital_cents=int(args.capital * 100), seed=args.seed)
    organism.run(args.cycles)
    snap = organism.snapshot()

    if args.json:
        print(json.dumps(snap, indent=2))
        return

    print("=" * 64)
    print("AEAN — Autonomous Economic Actor Network")
    print("=" * 64)
    print(f"LLM provider        : {snap['llm_provider']} (live={snap['llm_live']})")
    print(f"Cycles run          : {snap['cycle']}")
    print(f"Initial capital     : {_fmt_money(snap['initial_capital_cents'])}")
    print(f"Net worth           : {_fmt_money(snap['net_worth_cents'])}")
    print(f"Treasury (liquid)   : {_fmt_money(snap['treasury_cents'])}")
    print(f"Cumulative ROI      : {snap['cumulative_roi'] * 100:,.1f}%")
    print(f"Portfolio ROI       : {snap['portfolio_roi'] * 100:,.1f}%")
    print(f"Cells active/killed/scaled : {snap['active_cells']}/{snap['killed_cells']}/{snap['scaled_cells']}")
    print(f"Governance blocks   : {snap['governance_blocks']}")
    print(f"EKG                 : {snap['ekg']}")
    print("-" * 64)
    val = snap["validation"]
    fw = val["epistemic_firewall"]
    rg = val["rgae"]
    cs = val["three_critic_stack"]
    print("Reality & validation layer:")
    print(f"  Epistemic firewall : {fw['signals_checked']} checked, {fw['signals_rejected']} rejected, avg cred {fw['avg_credibility']}")
    print(f"  RGAE pipeline      : {rg['assets_passed']}/{rg['assets_screened']} assets passed, {rg['calibration_updates']} calibrations")
    print(f"  Three-Critic Stack : {cs['approved']}/{cs['reviews']} approved, {cs['blocked']} blocked, {cs['avg_latency_ms']}ms avg")
    print("-" * 64)
    print("Top micro-cells by ROI:")
    for c in snap["cells"][:8]:
        print(f"  {c['status']:<7} {c['market']:<16} {c['segment']:<10} ROI={c['roi'] * 100:6.1f}%  rev={_fmt_money(c['revenue_cents'])}")
    print("-" * 64)
    print("Research insights:")
    for i in snap["insights"]:
        print(f"  [{i['kind']}] {i['subject']}: {i['detail']} (conf {i['confidence']})")


if __name__ == "__main__":
    main()
