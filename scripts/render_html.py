#!/usr/bin/env python3
"""ds-view/render_html.py — Render insights + metrics into dashboard HTML.

Reads:  input/insights.jsonl
        input/metrics.jsonl

Writes: output/dashboard.html
"""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>ds-view dashboard</title>
<style>
body {{ font-family: -apple-system, sans-serif; margin: 2rem; background: #0f0f23; color: #c0c0d0; }}
h1 {{ color: #fff; border-bottom: 2px solid #4f46e5; padding-bottom: .5rem; }}
h2 {{ color: #818cf8; margin-top: 2rem; }}
.metric {{ display: inline-block; background: #1e1e2e; padding: 1rem 1.5rem; margin: .5rem; border-radius: .5rem; }}
.metric .value {{ font-size: 2rem; font-weight: bold; color: #4f46e5; }}
.metric .label {{ font-size: .85rem; color: #6b7280; }}
.insight {{ padding: 1rem; margin: .5rem 0; border-radius: .5rem; background: #1e1e2e; border-left: 4px solid; }}
.insight.info {{ border-left-color: #3b82f6; }}
.insight.warning {{ border-left-color: #f59e0b; }}
.insight.error {{ border-left-color: #ef4444; }}
.severity {{ display: inline-block; padding: .2rem .5rem; border-radius: .25rem; font-size: .75rem; font-weight: bold; text-transform: uppercase; margin-right: .5rem; }}
.severity.info {{ background: #1e3a5f; color: #60a5fa; }}
.severity.warning {{ background: #451a03; color: #fbbf24; }}
.severity.error {{ background: #450a0a; color: #f87171; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
th, td {{ padding: .5rem 1rem; text-align: left; border-bottom: 1px solid #2e2e3e; }}
th {{ color: #818cf8; }}
.meta {{ color: #6b7280; font-size: .85rem; margin-top: 2rem; }}
</style>
</head>
<body>
<h1>🔭 ds-view dashboard</h1>
<p class="meta">Generated: {generated_at} | Source: ds-core output/</p>

<h2>📊 Global Metrics</h2>
<div class="metrics">
{metrics_html}
</div>

<h2>💡 Insights</h2>
<div class="insights">
{insights_html}
</div>

<h2>📋 Device Breakdown</h2>
<table>
<tr><th>Device</th><th>Metric</th><th>Value</th></tr>
{device_rows}
</table>

</body>
</html>
"""

def render(input_dir, output_file):
    input_dir = Path(input_dir)
    
    insights = []
    if (input_dir / "insights.jsonl").exists():
        with open(input_dir / "insights.jsonl") as f:
            for line in f:
                if line.strip():
                    insights.append(json.loads(line))
    
    metrics = []
    if (input_dir / "metrics.jsonl").exists():
        with open(input_dir / "metrics.jsonl") as f:
            for line in f:
                if line.strip():
                    metrics.append(json.loads(line))
    
    # Global metrics
    metrics_html = ""
    for m in metrics:
        if m.get("device") == "global":
            metrics_html += f'''<div class="metric">
    <div class="value">{m["value"]:,}</div>
    <div class="label">{m["name"]} ({m.get("unit", "")})</div>
</div>'''
    if not metrics_html:
        metrics_html = "<p>No global metrics.</p>"
    
    # Insights
    insights_html = ""
    for ins in insights:
        sev = ins.get("severity", "info")
        insights_html += f'''<div class="insight {sev}">
    <span class="severity {sev}">{sev}</span>
    <strong>{ins["category"]}</strong>: {ins["message"]}
</div>'''
    if not insights_html:
        insights_html = "<p>No insights.</p>"
    
    # Device metrics table
    device_rows = ""
    for m in metrics:
        if m.get("device") != "global":
            device_rows += f"<tr><td>{m['device']}</td><td>{m['name']}</td><td>{m['value']:,} {m.get('unit', '')}</td></tr>"
    if not device_rows:
        device_rows = "<tr><td colspan=3>No device-level metrics.</td></tr>"
    
    html = HTML_TEMPLATE.format(
        generated_at=datetime.now().isoformat(),
        metrics_html=metrics_html,
        insights_html=insights_html,
        device_rows=device_rows
    )
    
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(html)
    
    print(f"Rendered: {output_file}")
    print(f"  Insights: {len(insights)}")
    print(f"  Metrics:  {len(metrics)}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="../ds-core/output")
    ap.add_argument("--output", default="./output/dashboard.html")
    args = ap.parse_args()
    render(args.input, args.output)
