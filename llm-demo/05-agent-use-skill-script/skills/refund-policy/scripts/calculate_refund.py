#!/usr/bin/env python3
"""Deterministic refund calculator used by the refund-policy skill."""

from __future__ import annotations

import argparse
import json
import sys

REASON_RATES: dict[str, tuple[float, bool]] = {
    "defect": (1.0, True),
    "wrong_item": (1.0, True),
    "change_mind": (0.8, False),
    "late_delivery": (0.5, True),
}

TIER_BONUS: dict[str, float] = {
    "gold": 0.10,
    "silver": 0.05,
    "bronze": 0.0,
}


def calculate(unit_price: float, qty: int, reason: str, membership: str) -> dict:
    reason_key = reason.strip().lower()
    tier_key = membership.strip().lower()

    if reason_key not in REASON_RATES:
        return {
            "error": f"unknown reason '{reason}'",
            "allowed_reasons": sorted(REASON_RATES),
        }
    if tier_key not in TIER_BONUS:
        return {
            "error": f"unknown membership '{membership}'",
            "allowed_memberships": sorted(TIER_BONUS),
        }

    rate, bonus_allowed = REASON_RATES[reason_key]
    subtotal = round(unit_price * qty, 2)
    after_rate = round(subtotal * rate, 2)
    bonus_rate = TIER_BONUS[tier_key] if bonus_allowed else 0.0
    bonus = round(after_rate * bonus_rate, 2)
    total = round(after_rate + bonus, 2)

    return {
        "unit_price": unit_price,
        "qty": qty,
        "reason": reason_key,
        "membership": tier_key,
        "subtotal": subtotal,
        "rate": rate,
        "after_rate": after_rate,
        "bonus_allowed": bonus_allowed,
        "bonus_rate": bonus_rate,
        "bonus": bonus,
        "refund_total": total,
        "currency": "USD",
        "policy": (
            f"{reason_key} → {int(rate * 100)}% of subtotal"
            + (f", {tier_key} bonus +{int(bonus_rate * 100)}%" if bonus_allowed else ", no membership bonus")
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate refund by policy")
    parser.add_argument("--unit-price", type=float, required=True)
    parser.add_argument("--qty", type=int, required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--membership", required=True)
    args = parser.parse_args()

    result = calculate(args.unit_price, args.qty, args.reason, args.membership)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if "error" in result else 0


if __name__ == "__main__":
    sys.exit(main())
