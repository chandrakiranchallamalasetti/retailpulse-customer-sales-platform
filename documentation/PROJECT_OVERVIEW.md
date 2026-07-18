# RetailPulse Project Overview

## Business problem
A sales organization needs one place to track customers, account owners, orders, products, and line-item revenue, then turn that data into decisions about growth, customer value, product demand, geography, and salesperson performance.

## Solution
RetailPulse combines a normalized relational model, reusable analytical views, Python analytics, and an interactive Streamlit application.

## Demo data
- 25 salespeople
- 25 customers
- 50 products
- 600 orders
- 1,275 order lines
- $542,553.99 modeled sales

The original 25 orders and 50 order lines are preserved from the source SQL. Additional deterministic synthetic records make the dashboard substantial enough for filtering and trend analysis. Synthetic data is clearly labeled in the `orders.data_origin` field.

## Core capabilities
- Executive KPIs and date/state/salesperson filters
- Monthly, state, product, category, and salesperson analysis
- Customer 360 and sales-team drilldowns
- Read-only SQL explorer
- Session-only live order simulation
- SQLite deployment database and SQL Server reference schema
- Automated tests and GitHub Actions CI
- GitHub Pages overview site

## Portfolio positioning
Present this as a **modernization of a team academic database project**, not as a production system processing real customer data. Retain the original team attribution in `SOURCE_MAPPING.md` and explain your own modernization contributions accurately.
