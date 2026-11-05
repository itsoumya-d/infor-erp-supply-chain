from __future__ import annotations

from collections import defaultdict

from inforops.models import Movement, PurchaseOrder


def receive_purchase_order(po: PurchaseOrder) -> list[Movement]:
    if po.status != "open":
        raise ValueError("purchase order is not open")
    return [Movement(line.item_id, line.quantity, "receipt", po.po_id) for line in po.lines]


def on_hand(movements: list[Movement]) -> dict[str, float]:
    balances: dict[str, float] = defaultdict(float)
    for movement in movements:
        sign = 1 if movement.movement_type in {"receipt", "adjustment_in"} else -1
        balances[movement.item_id] += sign * movement.quantity
    return {item: round(qty, 4) for item, qty in sorted(balances.items())}


def reconcile(expected: dict[str, float], movements: list[Movement]) -> list[dict]:
    actual = on_hand(movements)
    keys = sorted(set(expected) | set(actual))
    out = []
    for key in keys:
        exp, act = expected.get(key, 0.0), actual.get(key, 0.0)
        if exp != act:
            out.append({"item_id": key, "expected": exp, "actual": act, "variance": round(act - exp, 4)})
    return out
