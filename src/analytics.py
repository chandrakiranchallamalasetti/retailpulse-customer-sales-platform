from __future__ import annotations

import pandas as pd


def kpis(facts: pd.DataFrame) -> dict[str, float | int]:
    if facts.empty:
        return {"sales": 0.0, "orders": 0, "customers": 0, "aov": 0.0, "units": 0}
    sales = float(facts["line_revenue"].sum())
    orders = int(facts["order_id"].nunique())
    return {
        "sales": sales,
        "orders": orders,
        "customers": int(facts["customer_id"].nunique()),
        "aov": sales / orders if orders else 0.0,
        "units": int(facts["quantity"].sum()),
    }


def monthly_sales(facts: pd.DataFrame) -> pd.DataFrame:
    if facts.empty:
        return pd.DataFrame(columns=["month", "sales", "orders"])
    work = facts.assign(month=facts["order_date"].dt.to_period("M").dt.to_timestamp())
    return (
        work.groupby("month", as_index=False)
        .agg(sales=("line_revenue", "sum"), orders=("order_id", "nunique"))
        .sort_values("month")
    )


def grouped_sales(facts: pd.DataFrame, group: str, top_n: int | None = None) -> pd.DataFrame:
    if facts.empty:
        return pd.DataFrame(columns=[group, "sales", "orders", "units"])
    result = (
        facts.groupby(group, as_index=False)
        .agg(sales=("line_revenue", "sum"), orders=("order_id", "nunique"), units=("quantity", "sum"))
        .sort_values("sales", ascending=False)
    )
    return result.head(top_n) if top_n else result
