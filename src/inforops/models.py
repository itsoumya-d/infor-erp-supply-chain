from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Item:
    item_id: str
    description: str
    uom: str
    unit_cost: float


@dataclass
class BOMLine:
    parent_item: str
    component_item: str
    quantity: float


@dataclass
class PurchaseOrderLine:
    item_id: str
    quantity: float
    unit_cost: float


@dataclass
class PurchaseOrder:
    po_id: str
    supplier: str
    lines: list[PurchaseOrderLine]
    status: str = "open"


@dataclass
class Movement:
    item_id: str
    quantity: float
    movement_type: str
    reference: str


@dataclass
class QuoteLine:
    item_id: str
    quantity: float
    unit_price: float


@dataclass
class Quote:
    quote_id: str
    customer: str
    lines: list[QuoteLine]
    discount_pct: float = 0.0
    status: str = "draft"
