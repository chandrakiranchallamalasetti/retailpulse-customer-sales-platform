# RetailPulse — Customer Sales Analytics Platform

## Live Project

- [Live Streamlit Demo](https://retailpulse-customer-sales-platform-spse5im2uyvbdjnzdx7gsd.streamlit.app/)
- [Project Overview Website](https://chandrakiranchallamalasetti.github.io/retailpulse-customer-sales-platform/)

RetailPulse is a GitHub- and cloud-ready modernization of a customer sales database project. It combines normalized SQL, deterministic demo data, reusable analytics, an interactive Streamlit application, automated testing, and a static project overview site.

> **Attribution:** The source academic project credits Sameer Basha Md H, Brendan Gillow, and Chandra Kiran Challamalasetti. Keep the original team attribution and describe your modernization contribution separately.

## Highlights
- Five-table 3NF model: Salesperson, Customer, Product, Order, Order Item
- 50 products, 600 orders, and 1,275 order lines
- Executive dashboard with date, state, and salesperson filters
- Customer 360 and salesperson performance analysis
- Read-only SQL explorer
- Session-safe live transaction simulator
- SQLite deployment database plus SQL Server reference schema
- pytest suite and GitHub Actions CI
- Streamlit Community Cloud and GitHub Pages deployment paths

## Architecture
```text
Original SQL + notebooks + report + presentation
                      │
                      ▼
       Normalized schema + seed data + views
                      │
                      ▼
         Python query and analytics layers
                      │
                      ▼
 Streamlit app ── GitHub repo ── GitHub Pages site
```

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_database.py
streamlit run app.py
```

## Repository map
```text
app.py                      Streamlit application
src/                        Database, query, analytics, and UI helpers
data/customer_sales.db      Portable demo database
data/seed/                  Reproducible CSV seeds
sql/                        SQLite, SQL Server, views, and legacy SQL
notebooks/                  Quality checks and analytical walkthrough
scripts/                    Database build and exports
tests/                      Data integrity and safe-query tests
documentation/              Project, deployment, data, and interview guides
docs/                       GitHub Pages overview site
source_materials/           Original supplied artifacts
```

## Data lineage
The original source records are preserved with `data_origin = 'Source'`. The expanded dashboard data is deterministic and labeled `Synthetic demo`, making the project reproducible and transparent.

## Tests
```bash
pip install -r requirements-dev.txt
pytest -q
```

## Deployment
Follow [`documentation/DEPLOYMENT_GUIDE.md`](documentation/DEPLOYMENT_GUIDE.md) for exact GitHub, Streamlit Community Cloud, and GitHub Pages steps.

## Responsible portfolio use
This repository uses synthetic/demo data and is not a production customer system. Do not claim sole authorship of the original team project. Explain exactly which modernization, engineering, analytics, documentation, and deployment work you completed.
