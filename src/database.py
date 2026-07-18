from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Iterable

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "customer_sales.db"

READ_ONLY_PATTERN = re.compile(r"^\s*(SELECT|WITH|PRAGMA\s+table_info)\b", re.IGNORECASE)
FORBIDDEN_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|DETACH|REPLACE|VACUUM)\b",
    re.IGNORECASE,
)


def connect(db_path: Path | str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection with foreign-key enforcement enabled."""
    connection = sqlite3.connect(Path(db_path))
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def read_query(sql: str, params: Iterable[object] | None = None, db_path: Path | str = DEFAULT_DB_PATH) -> pd.DataFrame:
    """Execute a read query and return a DataFrame."""
    with connect(db_path) as connection:
        return pd.read_sql_query(sql, connection, params=tuple(params or ()))


def list_tables_and_views(db_path: Path | str = DEFAULT_DB_PATH) -> pd.DataFrame:
    return read_query(
        """
        SELECT name, type
        FROM sqlite_master
        WHERE type IN ('table', 'view')
          AND name NOT LIKE 'sqlite_%'
        ORDER BY type, name
        """,
        db_path=db_path,
    )


def safe_read_query(sql: str, db_path: Path | str = DEFAULT_DB_PATH, max_rows: int = 500) -> pd.DataFrame:
    """Run SELECT/WITH queries only, preventing mutation in the public demo."""
    cleaned = sql.strip().rstrip(";")
    if not cleaned:
        raise ValueError("Enter a SQL query.")
    if ";" in cleaned:
        raise ValueError("Only one SQL statement is allowed.")
    if not READ_ONLY_PATTERN.search(cleaned) or FORBIDDEN_PATTERN.search(cleaned):
        raise ValueError("The demo SQL editor accepts read-only SELECT or WITH queries.")
    wrapped = f"SELECT * FROM ({cleaned}) AS user_query LIMIT {int(max_rows)}"
    return read_query(wrapped, db_path=db_path)


def table_counts(db_path: Path | str = DEFAULT_DB_PATH) -> dict[str, int]:
    names = ["salespersons", "customers", "products", "orders", "order_items"]
    counts: dict[str, int] = {}
    with connect(db_path) as connection:
        for name in names:
            counts[name] = int(connection.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0])
    return counts
