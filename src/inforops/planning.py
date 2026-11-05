from __future__ import annotations

from collections import defaultdict

from inforops.models import BOMLine


def explode_bom(item_id: str, quantity: float, bom: list[BOMLine], depth: int = 10) -> dict[str, float]:
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    requirements: dict[str, float] = defaultdict(float)
    queue = [(item_id, quantity, 0)]
    while queue:
        parent, qty, level = queue.pop(0)
        if level > depth:
            raise ValueError("BOM depth exceeded")
        children = [line for line in bom if line.parent_item == parent]
        for line in children:
            required = qty * line.quantity
            requirements[line.component_item] += required
            queue.append((line.component_item, required, level + 1))
    return {k: round(v, 4) for k, v in sorted(requirements.items())}
