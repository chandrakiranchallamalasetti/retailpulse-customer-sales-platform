import pytest

from src.database import safe_read_query


def test_safe_read_query_allows_select():
    result = safe_read_query("SELECT state, COUNT(*) AS n FROM customers GROUP BY state")
    assert not result.empty


@pytest.mark.parametrize("statement", [
    "DELETE FROM customers",
    "DROP TABLE customers",
    "UPDATE customers SET state='MO'",
    "SELECT * FROM customers; SELECT * FROM orders",
])
def test_safe_read_query_blocks_mutation(statement):
    with pytest.raises(ValueError):
        safe_read_query(statement)
