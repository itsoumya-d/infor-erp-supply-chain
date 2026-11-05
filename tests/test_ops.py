from inforops.cpq import approve_quote, quote_total
from inforops.inventory import on_hand, receive_purchase_order, reconcile
from inforops.models import BOMLine, Movement, PurchaseOrder, PurchaseOrderLine, Quote, QuoteLine
from inforops.planning import explode_bom


def test_bom_explosion_nested():
    bom = [BOMLine("A", "B", 2), BOMLine("B", "C", 3), BOMLine("A", "D", 1)]
    result = explode_bom("A", 1, bom)
    assert result == {"B": 2.0, "C": 6.0, "D": 1.0}


def test_po_receipt_and_reconcile():
    po = PurchaseOrder("PO-1", "Steel Co", [PurchaseOrderLine("RM-1", 100, 10.0)])
    movements = receive_purchase_order(po)
    assert on_hand(movements) == {"RM-1": 100.0}
    mismatches = reconcile({"RM-1": 90.0}, movements)
    assert mismatches[0]["variance"] == 10.0


def test_quote_discount_and_approval():
    quote = Quote("Q-1", "Kauri", [QuoteLine("FG-1", 2, 500.0)], discount_pct=12.0)
    total = quote_total(quote)
    assert total["subtotal"] == 1000.0
    assert total["discount"] == 120.0
    assert total["net"] == 880.0
    result = approve_quote(quote)
    assert result["approval_required"] is True
    assert result["status"] == "pending_approval"
