from __future__ import annotations

from inforops.models import Quote


def quote_total(quote: Quote) -> dict:
    subtotal = round(sum(line.quantity * line.unit_price for line in quote.lines), 2)
    discount = round(subtotal * quote.discount_pct / 100.0, 2)
    net = round(subtotal - discount, 2)
    return {"subtotal": subtotal, "discount": discount, "net": net}


def approve_quote(quote: Quote, discount_threshold: float = 10.0) -> dict:
    total = quote_total(quote)
    needs_approval = quote.discount_pct > discount_threshold
    quote.status = "pending_approval" if needs_approval else "approved"
    return total | {"quote_id": quote.quote_id, "status": quote.status, "approval_required": needs_approval}
