# etf-ci-demo

A small project that supports my Professional Learning Report and Portfolio
(43030 Professional Practice in Computing). It covers three goals:

| Goal | What it shows | Where |
| --- | --- | --- |
| 3. Software development tools | Flask app, Dockerfile, GitHub Actions running PyTest | `app.py`, `Dockerfile`, `.github/workflows/main.yml`, `tests/` |
| 4. Data modelling | ERD, UML diagrams, data dictionary, SQL schema for a mock e-commerce system | `docs/` |
| 5. Financial data and Python | Mock ETF pipeline: load, clean, quality report, plot | `etf_pipeline.py` |

| Portfolio item | File(s) |
| --- | --- |
| P1 Repository and CI/CD workflow | `.github/workflows/main.yml`, `tests/test_pipeline.py` |
| P2 Dockerfile and Flask app | `Dockerfile`, `app.py` |
| P3 Docker bridge network diagram | `docs/diagrams/p3-docker-bridge-network.png` |
| P4 ERD, UML, data dictionary | `docs/diagrams/p4-*.png`, `docs/data_dictionary.md`, `docs/schema.sql` |
| P5 ETF pipeline script | `etf_pipeline.py` |
| P6 Data quality report and chart | `docs/diagrams/p6-cleaned-prices.png` (run the pipeline to reproduce) |

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

pytest -q                        # run the tests
python etf_pipeline.py --demo    # synthetic data, no network needed
python etf_pipeline.py           # real SPY/QQQ prices via yfinance (needs network)
python app.py                    # Flask on http://localhost:5000
```

Endpoints: `/health` returns `{"status": "ok"}`; `/quality` returns the data
quality report for the demo data as JSON.

## Run with Docker

```bash
docker network create etf-net
docker build -t etf-demo .
docker run -d --name flask-app --network etf-net -p 8000:5000 etf-demo
curl http://localhost:8000/health
```

Port 8000 on the host maps to port 5000 in the container. Other containers on
`etf-net` can reach the app by name (`http://flask-app:5000`).

## Notes

- The `--demo` data is synthetic, with deliberate gaps. Gaps up to 3 days are
  forward-filled; longer gaps are left missing and flagged, not hidden.
- This is a learning project, not production code.
