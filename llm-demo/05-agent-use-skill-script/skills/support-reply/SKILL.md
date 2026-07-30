---
name: support-reply
description: >
  Use when drafting customer-support replies in Chinese: apology emails,
  refund confirmation messages, or follow-up templates for e-commerce CS.
  Prefer the bundled draft_reply.py script to fill the official template.
---

# Support Reply Skill

## Workflow

1. Collect: `name`, `issue`, `action`（金额/订单号必须来自已确认事实）
2. **Run the script** to fill the official template:

```bash
python scripts/draft_reply.py \
  --name Alice \
  --issue "耳机质量问题退货" \
  --action "已按政策退款 195.80 USD，预计 3-5 个工作日到账"
```

3. 用脚本返回的 `email_body` 作为客服邮件正文；可微调语气，但不要改模板结构

## Tone

- 礼貌、简洁、共情，不卑不亢
- 先致歉 / 确认问题，再给解决方案，最后给下一步

## Constraints

- 不要承诺无法兑现的时效或金额
- 金额与订单号必须来自用户已提供的事实，不得编造
- 全文使用简体中文
