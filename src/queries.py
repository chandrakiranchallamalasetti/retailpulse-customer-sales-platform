from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Sequence

import pandas as pd

from .database import DEFAULT_DB_PATH, read_query


def _filters(start_date: date, end_date: date, states: Sequence[str], salespersons: Sequence[str]):
    clauses = ["date(order_date) BETWEEN date(?) AND date(?)"]
    params: list[object] = [start_date.isoformat(), end_date.isoformat()]
    if states:
        clauses.append(f"state IN ({','.join('?' for _ in states)})")
        params.extend(states)
    if salespersons:
        clauses.append(f"salesperson_name IN ({','.join('?' for _ in salespersons)})")
        params.extend(salespersons)
    return " AND ".join(clauses), params


def dimensions(db_path: Path | str = DEFAULT_DB_PATH) -> dict[str, list[str] | date]:
    dates = read_query("SELECT MIN(order_date) min_date, MAX(order_date) max_date FROM orders", db_path=db_path)
    states = read_query("SELECT DISTINCT state FROM customers ORDER BY state", db_path=db_path)["state"].tolist()
    salespersons = read_query(
        "SELECT first_name || ' ' || last_name AS name FROM salespersons ORDER BY name",
        db_path=db_path,
    )["name"].tolist()
    return {
        "min_date": pd.to_datetime(dates.loc[0, "min_date"]).date(),
        "max_date": pd.to_datetime(dates.loc[0, "max_date"]).date(),
        "states": states,
        "salespersons": salespersons,
    }


def sales_facts(start_date: date, end_date: date, states: Sequence[str] = (), salespersons: Sequence[str] = (), db_path: Path | str = DEFAULT_DB_PATH) -> pd.DataFrame:
    where, params = _filters(start_date, end_date, states, salespersons)
    df = read_query(f"SELECT * FROM vw_sales_facts WHERE {where}", params, db_path)
    if not df.empty:
        df["order_date"] = pd.to_datetime(df["order_date"])
    return df


def customer_summary(db_path: Path | str = DEFAULT_DB_PATH) -> pd.DataFrame:
    return read_query("SELECT * FROM vw_customer_summary ORDER BY total_sales DESC", db_path=db_path)


def salesperson_summary(db_path: Path | str = DEFAULT_DB_PATH) -> pd.DataFrame:
    return read_query("SELECT * FROM vw_salesperson_performance ORDER BY total_sales DESC", db_path=db_path)


def product_summary(db_path: Path | str = DEFAULT_DB_PATH) -> pd.DataFrame:
    return read_query("SELECT * FROM vw_product_performance ORDER BY total_sales DESC", db_path=db_path)
