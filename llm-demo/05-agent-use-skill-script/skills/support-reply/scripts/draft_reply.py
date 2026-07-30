#!/usr/bin/env python3
"""Fill the support-reply email template used by the support-reply skill."""

from __future__ import annotations

import argparse
import json
import sys


TEMPLATE = """尊敬的 {name}：

感谢您联系我们。关于您反馈的 {issue}，我们已完成核查。

处理结果：
- {action}

如有其他问题，请随时回复本邮件。

此致
客服团队"""


def draft(name: str, issue: str, action: str) -> dict:
    body = TEMPLATE.format(name=name.strip(), issue=issue.strip(), action=action.strip())
    return {
        "name": name.strip(),
        "issue": issue.strip(),
        "action": action.strip(),
        "email_body": body,
        "language": "zh-CN",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft a Chinese CS reply email")
    parser.add_argument("--name", required=True, help="Customer name")
    parser.add_argument("--issue", required=True, help="Issue description")
    parser.add_argument("--action", required=True, help="Resolution / action taken")
    args = parser.parse_args()

    result = draft(args.name, args.issue, args.action)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
