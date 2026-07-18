from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "customer_sales.db"
SEED = ROOT / "data" / "seed"


def rows(name: str):
    with (SEED / f"{name}.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_database() -> Path:
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript((ROOT / "sql" / "schema_sqlite.sql").read_text(encoding="utf-8"))
    conn.executemany(
        "INSERT INTO salespersons VALUES (:salesperson_id,:first_name,:last_name)", rows("salespersons")
    )
    conn.executemany(
        "INSERT INTO customers VALUES (:customer_id,:customer_name,:state,:salesperson_id)", rows("customers")
    )
    conn.executemany(
        "INSERT INTO products VALUES (:product_id,:product_name,:category,:list_price)", rows("products")
    )
    conn.executemany(
        "INSERT INTO orders VALUES (:order_id,:order_date,:customer_id,:order_status,:data_origin)", rows("orders")
    )
    conn.executemany(
        "INSERT INTO order_items VALUES (:order_item_id,:order_id,:product_id,:quantity,:unit_price)", rows("order_items")
    )
    conn.executescript((ROOT / "sql" / "analytics_views_sqlite.sql").read_text(encoding="utf-8"))
    conn.commit()
    conn.close()
    print(f"Built {DB_PATH}")
    return DB_PATH


if __name__ == "__main__":
    build_database()
