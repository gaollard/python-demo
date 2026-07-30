---
name: refund-policy
description: >
  Use when calculating refunds, explaining return/refund rules, or deciding
  refund amounts by membership tier and reason (defect, change_mind, late_delivery).
  Prefer the bundled calculate_refund.py script over mental math.
---

# Refund Policy Skill

## Workflow

1. Collect: `unit_price`, `qty`, `reason`, `membership`
2. **Run the script** (do not re-implement the formula yourself):

```bash
python scripts/calculate_refund.py \
  --unit-price 89 --qty 2 --reason defect --membership gold
```

3. Use the JSON output (`refund_total`, `policy`, steps) to answer in Chinese

## Allowed values

| field | values |
|-------|--------|
| reason | `defect`, `wrong_item`, `change_mind`, `late_delivery` |
| membership | `gold`, `silver`, `bronze` |

## Output format

Always reply in Chinese with:

1. 计算过程（小计 → 比例 → 加成 → 合计）— 引用脚本输出字段
2. 最终退款金额（USD，保留两位小数）— 使用 `refund_total`
3. 一句政策依据说明 — 使用 `policy`

Do not invent other rates. If reason is unknown, ask the user to clarify.
