from src.database import connect, table_counts


def test_core_tables_are_populated():
    counts = table_counts()
    assert counts["salespersons"] == 25
    assert counts["customers"] == 25
    assert counts["products"] >= 40
    assert counts["orders"] == 600
    assert counts["order_items"] > counts["orders"]


def test_foreign_keys_have_no_violations():
    with connect() as connection:
        violations = connection.execute("PRAGMA foreign_key_check").fetchall()
    assert violations == []


def test_sales_fact_view_has_revenue():
    with connect() as connection:
        total = connection.execute("SELECT SUM(line_revenue) FROM vw_sales_facts").fetchone()[0]
    assert total > 0
