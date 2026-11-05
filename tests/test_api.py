from fastapi.testclient import TestClient

from inforops.api import app
from inforops.generate import demo

client = TestClient(app)


def test_bom_endpoint():
    payload = demo()
    response = client.post("/bom/explode?item_id=FG-100&quantity=1", json=payload["bom"])
    assert response.status_code == 200
    assert response.json()["RM-300"] == 6.0


def test_quote_endpoint():
    response = client.post("/quotes/approve", json=demo()["quote"])
    assert response.status_code == 200
    assert response.json()["approval_required"] is True


def test_inventory_endpoint():
    payload = demo()
    response = client.post("/inventory/reconcile", json={"expected": {"RM-300": 90.0}, "movements": payload["movements"]})
    assert response.status_code == 200
    assert response.json()[0]["variance"] == 10.0
