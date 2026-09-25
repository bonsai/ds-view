# ds-view

Display layer (component 3/3 of kankyou-hub). Renders ds-insighter JSONL output.

## Interface

**Input**: `ds-insighter/output/` (or any directory with insights.jsonl + metrics.jsonl)

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
# After ds-insighter produces output/
ds-view cli --input ../ds-insighter/output
ds-view html --input ../ds-insighter/output --output ./output/dashboard.html
DS_PORT=3000 ds-view serve
```

## Related

- **ds-insighter** → provides insights.jsonl + metrics.jsonl
