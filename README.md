# ds-view

Display layer (component 3/3 of ds-dashboard). Renders ds-core JSONL output.

## Interface

**Input**: `ds-core/output/` (or any directory with insights.jsonl + metrics.jsonl)

**Output**:
```
output/dashboard.html   — interactive HTML dashboard
cli                     — terminal display
```

## Commands

```bash
ds-view html     # render HTML dashboard
ds-view cli      # terminal display
ds-view serve    # local HTTP server (port 8080)
```

## Example

```bash
# After ds-core produces output/
ds-view cli --input ../ds-core/output
ds-view html --input ../ds-core/output --output ./output/dashboard.html
DS_PORT=3000 ds-view serve
```

## Related

- **ds-core** → provides insights.jsonl + metrics.jsonl
