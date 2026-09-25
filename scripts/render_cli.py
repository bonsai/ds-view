#!/usr/bin/env python3
"""ds-view/render_cli.py — CLI display of ds-core insights + metrics.

Reads: input/insights.jsonl, input/metrics.jsonl
"""
import argparse, json
from pathlib import Path

def render_cli(input_dir):
    input_dir = Path(input_dir)
    
    # Load insights
    insights = []
    if (input_dir / "insights.jsonl").exists():
        with open(input_dir / "insights.jsonl") as f:
            for line in f:
                if line.strip():
                    insights.append(json.loads(line))
    
    # Load metrics
    metrics = []
    if (input_dir / "metrics.jsonl").exists():
        with open(input_dir / "metrics.jsonl") as f:
            for line in f:
                if line.strip():
                    metrics.append(json.loads(line))
    
    print("═" * 50)
    print("  🔭 ds-view CLI")
    print("═" * 50)
    
    # Global metrics
    print("\n📊 Global Metrics")
    print("─" * 40)
    globals = [m for m in metrics if m.get("device") == "global"]
    for m in globals:
        print(f"  {m['name']:25s} {m['value']:>10,} {m.get('unit', '')}")
    
    # Device metrics
    device_metrics = [m for m in metrics if m.get("device") != "global"]
    if device_metrics:
        print("\n📋 Per-Device Metrics")
        print("─" * 40)
        for m in device_metrics:
            print(f"  {m['device']:10s} {m['name']:20s} {m['value']:>10,} {m.get('unit', '')}")
    
    # Insights
    print("\n💡 Insights")
    print("─" * 40)
    for ins in insights:
        sev = ins.get("severity", "info").upper()
        icon = {"INFO": "ℹ️", "WARNING": "⚠️", "ERROR": "❌"}.get(sev, "•")
        print(f"  {icon} [{sev}] {ins['category']}")
        print(f"     {ins['message']}")
        if ins.get("data"):
            for k, v in ins["data"].items():
                if isinstance(v, list) and v:
                    print(f"     {k}: {', '.join(str(x) for x in v[:5])}{'...' if len(v) > 5 else ''}")
    
    # Summary
    print("\n" + "═" * 50)
    print(f"  {len(insights)} insights | {len(metrics)} metrics")
    print("═" * 50)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="../ds-core/output")
    args = ap.parse_args()
    render_cli(args.input)
