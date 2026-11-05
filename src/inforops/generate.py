from __future__ import annotations

import json
from pathlib import Path


def demo() -> dict:
    return {
        "bom": [
            {"parent_item": "FG-100", "component_item": "SA-200", "quantity": 2},
            {"parent_item": "SA-200", "component_item": "RM-300", "quantity": 3},
            {"parent_item": "FG-100", "component_item": "PK-400", "quantity": 1},
        ],
        "quote": {
            "quote_id": "Q-1", "customer": "Kauri Manufacturing",
            "lines": [
                {"item_id": "FG-100", "quantity": 10, "unit_price": 450.0},
                {"item_id": "SA-200", "quantity": 5, "unit_price": 220.0},
            ],
            "discount_pct": 12.0,
        },
        "purchase_order": {
            "po_id": "PO-1", "supplier": "Steel Co",
            "lines": [{"item_id": "RM-300", "quantity": 120, "unit_cost": 18.5}],
        },
        "expected": {"RM-300": 100.0},
        "movements": [
            {"item_id": "RM-300", "quantity": 120, "movement_type": "receipt", "reference": "PO-1"},
            {"item_id": "RM-300", "quantity": 20, "movement_type": "issue", "reference": "WO-1"},
        ],
    }


def main() -> None:
    path = Path("data/demo.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(demo(), indent=2))
    print(path)


if __name__ == "__main__":
    main()
