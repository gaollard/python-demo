---
name: refund-policy
description: >
  Use when calculating refunds, explaining return/refund rules, or deciding
  refund amounts by membership tier and reason (defect, change_mind, late_delivery).
---

# Refund Policy Skill

## Rules

Base amount = `unit_price * qty`.

| reason | base rate | membership bonus |
|--------|-----------|------------------|
| defect / wrong_item | 100% | yes |
| change_mind | 80% | no |
| late_delivery | 50% | yes |

Membership bonus rates:

- gold: +10% of (base amount after rate)
- silver: +5%
- bronze: +0%

## Output format

Always reply in Chinese with:

1. 计算过程（小计 → 比例 → 加成 → 合计）
2. 最终退款金额（USD，保留两位小数）
3. 一句政策依据说明

Do not invent other rates. If reason is unknown, ask the user to clarify.
