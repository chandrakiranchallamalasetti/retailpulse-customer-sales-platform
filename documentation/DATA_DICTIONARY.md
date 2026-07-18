# Data Dictionary

## `salespersons`
| Column | Type | Description |
|---|---|---|
| salesperson_id | INTEGER | Primary key |
| first_name | TEXT | Given name |
| last_name | TEXT | Family name |

## `customers`
| Column | Type | Description |
|---|---|---|
| customer_id | INTEGER | Primary key |
| customer_name | TEXT | Customer/company name |
| state | TEXT | Two-character U.S. state code |
| salesperson_id | INTEGER | Assigned salesperson foreign key |

## `products`
| Column | Type | Description |
|---|---|---|
| product_id | INTEGER | Primary key |
| product_name | TEXT | Unique product name |
| category | TEXT | Product category |
| list_price | REAL | Reference price used by demo generation |

## `orders`
| Column | Type | Description |
|---|---|---|
| order_id | INTEGER | Primary key |
| order_date | TEXT | ISO date |
| customer_id | INTEGER | Customer foreign key |
| order_status | TEXT | Completed, Shipped, or Pending |
| data_origin | TEXT | Source or Synthetic demo |

## `order_items`
| Column | Type | Description |
|---|---|---|
| order_item_id | INTEGER | Primary key |
| order_id | INTEGER | Order foreign key |
| product_id | INTEGER | Product foreign key |
| quantity | INTEGER | Units sold |
| unit_price | REAL | Transaction price |

## Main analytical view
`vw_sales_facts` joins all five entities and calculates `line_revenue = quantity × unit_price`. Other views aggregate customer, salesperson, product, state, and monthly performance.
