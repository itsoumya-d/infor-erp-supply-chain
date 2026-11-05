# infor-erp-supply-chain

[![ci](https://github.com/itsoumya-d/infor-erp-supply-chain/actions/workflows/ci.yml/badge.svg)](https://github.com/itsoumya-d/infor-erp-supply-chain/actions/workflows/ci.yml)

A tested reference for Infor-shaped ERP manufacturing and distribution
workflows:

- Multi-level BOM explosion.
- Purchase-order receipt into inventory movements.
- On-hand balances and inventory reconciliation.
- Quote pricing, discounting and approval thresholds (CPQ).
- FastAPI surface and synthetic demo data.

This is a **reference implementation**, not a claim of production Infor M3,
Infor LN or ERP consulting experience. No live ERP, EDI or supplier system is
used in CI.

## Run

```bash
uv venv --python 3.12
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn inforops.api:app --reload
python -m inforops.generate
```

## License

MIT
