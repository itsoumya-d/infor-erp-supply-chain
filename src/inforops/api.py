from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from inforops.cpq import approve_quote
from inforops.inventory import receive_purchase_order, reconcile
from inforops.models import BOMLine, Movement, PurchaseOrder, PurchaseOrderLine, Quote, QuoteLine
from inforops.planning import explode_bom

app = FastAPI(title="Infor ERP supply chain", version="0.1.0")


class BOMLineIn(BaseModel):
    parent_item: str
    component_item: str
    quantity: float


class QuoteLineIn(BaseModel):
    item_id: str
    quantity: float
    unit_price: float


class QuoteIn(BaseModel):
    quote_id: str
    customer: str
    lines: list[QuoteLineIn]
    discount_pct: float = 0.0


class POLineIn(BaseModel):
    item_id: str
    quantity: float
    unit_cost: float


class POIn(BaseModel):
    po_id: str
    supplier: str
    lines: list[POLineIn]


class MovementIn(BaseModel):
    item_id: str
    quantity: float
    movement_type: str
    reference: str = ""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/bom/explode")
def bom_explode(item_id: str, quantity: float, bom: list[BOMLineIn]) -> dict[str, float]:
    return explode_bom(item_id, quantity, [BOMLine(**b.model_dump()) for b in bom])


@app.post("/quotes/approve")
def quote_approve(payload: QuoteIn) -> dict:
    quote = Quote(payload.quote_id, payload.customer, [QuoteLine(**l.model_dump()) for l in payload.lines], payload.discount_pct)
    return approve_quote(quote)


@app.post("/purchase-orders/receive")
def po_receive(payload: POIn) -> list[dict]:
    po = PurchaseOrder(payload.po_id, payload.supplier, [PurchaseOrderLine(**l.model_dump()) for l in payload.lines])
    return [m.__dict__ for m in receive_purchase_order(po)]


@app.post("/inventory/reconcile")
def inventory_reconcile(expected: dict[str, float], movements: list[MovementIn]) -> list[dict]:
    return reconcile(expected, [Movement(**m.model_dump()) for m in movements])
