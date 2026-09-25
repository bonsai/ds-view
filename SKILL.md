---
name: ds-view
description: 表示層。ds-insighter の insights.jsonl + metrics.jsonl を読み込み、HTMLダッシュボードまたはCLI表示にレンダリングする。「ダッシュボード表示」「insights可視化」「メトリクス表示」「render」「ds-view」で発動。
---

# ds-view

表示層。ds-insighter の JSONL output を HTML / CLI にレンダリングする。

- リポジトリ: `/home/bons/repos/ds-view`
- CLI: `bin/ds-view`

## Commands

```bash
ds-view html     # → output/dashboard.html
ds-view cli      # → terminal display
ds-view serve    # → localhost:8080
```

## Input

`ds-insighter/output/`:
- `insights.jsonl`
- `metrics.jsonl`

## Output

| 形式 | ファイル/動作 |
|------|-------------|
| HTML | `output/dashboard.html` (dark theme, responsive) |
| CLI | カラー付きターミナル出力 |
| HTTP | `python3 -m http.server` |

## Related

- **ds-insighter** → input提供
- **kenja** → 別経路で同じinsightsを発話利用
