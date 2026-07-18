from __future__ import annotations

import random
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics import grouped_sales, kpis, monthly_sales
from src.components import hero, inject_css, section_card
from src.database import list_tables_and_views, read_query, safe_read_query, table_counts
from src.queries import customer_summary, dimensions, product_summary, sales_facts, salesperson_summary

st.set_page_config(
    page_title="RetailPulse | Customer Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

@st.cache_data(show_spinner=False)
def get_dimensions():
    return dimensions()

@st.cache_data(show_spinner=False)
def get_facts(start_date, end_date, states, salespersons):
    return sales_facts(start_date, end_date, states, salespersons)

@st.cache_data(show_spinner=False)
def get_customer_summary():
    return customer_summary()

@st.cache_data(show_spinner=False)
def get_salesperson_summary():
    return salesperson_summary()

@st.cache_data(show_spinner=False)
def get_product_summary():
    return product_summary()

@st.cache_data(show_spinner=False)
def get_table_counts():
    return table_counts()

@st.cache_data(show_spinner=False)
def get_entities():
    customers = read_query("SELECT customer_id, customer_name, state FROM customers ORDER BY customer_name")
    products = read_query("SELECT product_id, product_name, category, list_price FROM products ORDER BY product_name")
    return customers, products


def money(value: float) -> str:
    return f"${value:,.0f}"


def render_metrics(facts: pd.DataFrame):
    values = kpis(facts)
    cols = st.columns(5)
    cols[0].metric("Sales", money(values["sales"]))
    cols[1].metric("Orders", f'{values["orders"]:,}')
    cols[2].metric("Customers", f'{values["customers"]:,}')
    cols[3].metric("Average order", money(values["aov"]))
    cols[4].metric("Units sold", f'{values["units"]:,}')


def base_chart_layout(fig, height=420):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=45, b=10), legend_title_text="")
    return fig


dims = get_dimensions()

st.sidebar.markdown("## RetailPulse")
st.sidebar.caption("Customer orders database + interactive analytics")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Executive Dashboard", "Customer 360", "Sales Team", "Data Explorer", "Live Demo Lab", "Project Guide"],
)
st.sidebar.divider()
st.sidebar.caption("Portfolio demo data: original course records plus a deterministic synthetic extension.")

if page == "Overview":
    hero(
        "RetailPulse Customer Sales Platform",
        "A deployment-ready modernization of the Customer Sales Database System: normalized relational storage, reusable SQL views, Python analytics, an interactive Streamlit application, and a GitHub Pages project site.",
    )
    counts = get_table_counts()
    facts = get_facts(dims["min_date"], dims["max_date"], (), ())
    render_metrics(facts)
    st.markdown("### What this project demonstrates")
    c1, c2, c3 = st.columns(3)
    with c1:
        section_card("Database engineering", "Five-table 3NF design, foreign keys, indexes, SQL views, a SQL Server reference implementation, and a portable SQLite demo database.")
    with c2:
        section_card("Analytics engineering", "Reusable query layer, KPI calculations, time-series analysis, customer 360 views, product performance, and salesperson performance.")
    with c3:
        section_card("Data application", "Interactive filters, responsive charts, read-only SQL explorer, session-safe live order simulation, documentation, tests, and CI.")

    st.markdown("### Architecture")
    a1, a2, a3, a4 = st.columns([1, .2, 1, .2])
    with a1:
        st.markdown("**Source layer**")
        st.write("SQL Server DDL/DML, Python notebooks, report, presentation")
    with a2:
        st.markdown("## →")
    with a3:
        st.markdown("**Data layer**")
        st.write("SQLite demo DB + normalized SQL Server schema + analytical views")
    with a4:
        st.markdown("## →")
    b1, b2 = st.columns([1, 1])
    with b1:
        st.markdown("**Application layer**")
        st.write("Streamlit, pandas, Plotly, safe SQL explorer")
    with b2:
        st.markdown("**Delivery layer**")
        st.write("GitHub repository, CI workflow, Streamlit Cloud, GitHub Pages")

    st.info("The source report describes a normalized sales database, Python-based insertion, and sales visualizations. This version preserves those goals while resolving the source's four-table/five-table inconsistency by introducing a dedicated Product table.")

elif page == "Executive Dashboard":
    hero("Executive Dashboard", "Filter the full sales fact view and explore trends by month, state, product, category, customer, and salesperson.")
    with st.sidebar:
        st.markdown("### Dashboard filters")
        date_value = st.date_input("Order date", value=(dims["min_date"], dims["max_date"]), min_value=dims["min_date"], max_value=dims["max_date"])
        if isinstance(date_value, tuple) and len(date_value) == 2:
            start_date, end_date = date_value
        else:
            start_date, end_date = dims["min_date"], dims["max_date"]
        states = st.multiselect("State", dims["states"])
        reps = st.multiselect("Salesperson", dims["salespersons"])
    facts = get_facts(start_date, end_date, tuple(states), tuple(reps))
    render_metrics(facts)
    if facts.empty:
        st.warning("No records match the selected filters.")
    else:
        monthly = monthly_sales(facts)
        state = grouped_sales(facts, "state")
        product = grouped_sales(facts, "product_name", 10)
        category = grouped_sales(facts, "category")
        rep = grouped_sales(facts, "salesperson_name", 10)

        left, right = st.columns([1.35, 1])
        with left:
            fig = px.line(monthly, x="month", y="sales", markers=True, title="Monthly sales", labels={"month": "Month", "sales": "Sales (USD)"})
            st.plotly_chart(base_chart_layout(fig), use_container_width=True)
        with right:
            fig = px.bar(state, x="state", y="sales", title="Sales by state", labels={"state": "State", "sales": "Sales (USD)"})
            st.plotly_chart(base_chart_layout(fig), use_container_width=True)

        left, right = st.columns(2)
        with left:
            fig = px.bar(product.sort_values("sales"), x="sales", y="product_name", orientation="h", title="Top 10 products", labels={"product_name": "Product", "sales": "Sales (USD)"})
            st.plotly_chart(base_chart_layout(fig), use_container_width=True)
        with right:
            fig = px.treemap(category, path=["category"], values="sales", title="Category mix")
            st.plotly_chart(base_chart_layout(fig), use_container_width=True)

        fig = px.bar(rep.sort_values("sales"), x="sales", y="salesperson_name", orientation="h", title="Top salespeople", labels={"salesperson_name": "Salesperson", "sales": "Sales (USD)"})
        st.plotly_chart(base_chart_layout(fig, 500), use_container_width=True)

        st.markdown("### Recent orders")
        recent = (
            facts.groupby(["order_id", "order_date", "customer_name", "state", "salesperson_name"], as_index=False)
            .agg(order_total=("line_revenue", "sum"), items=("product_id", "count"))
            .sort_values(["order_date", "order_id"], ascending=False)
            .head(25)
        )
        st.dataframe(recent, use_container_width=True, hide_index=True, column_config={"order_total": st.column_config.NumberColumn(format="$%.2f")})

elif page == "Customer 360":
    hero("Customer 360", "Review account ownership, total value, purchasing history, category mix, and recent orders for a selected customer.")
    summary = get_customer_summary()
    selected_name = st.selectbox("Customer", summary["customer_name"].tolist())
    selected = summary.loc[summary["customer_name"] == selected_name].iloc[0]
    facts = get_facts(dims["min_date"], dims["max_date"], (), ())
    customer_facts = facts.loc[facts["customer_id"] == selected["customer_id"]].copy()
    cols = st.columns(4)
    cols[0].metric("Lifetime sales", money(selected["total_sales"]))
    cols[1].metric("Orders", int(selected["order_count"]))
    cols[2].metric("Average order", money(selected["avg_order_value"]))
    cols[3].metric("Last order", str(selected["last_order_date"]))
    st.caption(f'{selected["customer_name"]} · {selected["state"]} · Account owner: {selected["salesperson_name"]}')

    left, right = st.columns(2)
    with left:
        product = grouped_sales(customer_facts, "product_name", 10)
        fig = px.bar(product.sort_values("sales"), x="sales", y="product_name", orientation="h", title="Top products purchased")
        st.plotly_chart(base_chart_layout(fig), use_container_width=True)
    with right:
        category = grouped_sales(customer_facts, "category")
        fig = px.pie(category, names="category", values="sales", hole=.55, title="Category mix")
        st.plotly_chart(base_chart_layout(fig), use_container_width=True)

    order_history = (
        customer_facts.groupby(["order_id", "order_date", "order_status"], as_index=False)
        .agg(order_total=("line_revenue", "sum"), units=("quantity", "sum"), line_items=("product_id", "count"))
        .sort_values("order_date", ascending=False)
    )
    st.markdown("### Order history")
    st.dataframe(order_history, use_container_width=True, hide_index=True, column_config={"order_total": st.column_config.NumberColumn(format="$%.2f")})

elif page == "Sales Team":
    hero("Sales Team Performance", "Compare salesperson revenue, portfolio size, order volume, and average order value.")
    reps = get_salesperson_summary()
    st.dataframe(
        reps,
        use_container_width=True,
        hide_index=True,
        column_config={"total_sales": st.column_config.NumberColumn(format="$%.2f"), "avg_order_value": st.column_config.NumberColumn(format="$%.2f")},
    )
    selected_rep = st.selectbox("Salesperson detail", reps["salesperson_name"].tolist())
    facts = get_facts(dims["min_date"], dims["max_date"], (), (selected_rep,))
    render_metrics(facts)
    left, right = st.columns(2)
    with left:
        customers = grouped_sales(facts, "customer_name", 10)
        fig = px.bar(customers.sort_values("sales"), x="sales", y="customer_name", orientation="h", title="Top managed customers")
        st.plotly_chart(base_chart_layout(fig), use_container_width=True)
    with right:
        categories = grouped_sales(facts, "category")
        fig = px.pie(categories, names="category", values="sales", hole=.45, title="Sales category mix")
        st.plotly_chart(base_chart_layout(fig), use_container_width=True)

elif page == "Data Explorer":
    hero("Data Explorer", "Inspect normalized tables and analytical views or run a read-only SQL query against the included SQLite database.")
    objects = list_tables_and_views()
    left, right = st.columns([.8, 1.2])
    with left:
        st.markdown("### Database objects")
        st.dataframe(objects, use_container_width=True, hide_index=True)
        object_name = st.selectbox("Preview table/view", objects["name"].tolist())
        preview = read_query(f'SELECT * FROM "{object_name}" LIMIT 100')
        st.dataframe(preview, use_container_width=True, hide_index=True)
    with right:
        st.markdown("### Read-only SQL editor")
        default_sql = """SELECT state,\n       ROUND(SUM(line_revenue), 2) AS total_sales,\n       COUNT(DISTINCT order_id) AS orders\nFROM vw_sales_facts\nGROUP BY state\nORDER BY total_sales DESC"""
        sql = st.text_area("SQL", value=default_sql, height=220)
        if st.button("Run query", type="primary"):
            try:
                result = safe_read_query(sql)
                st.success(f"Returned {len(result):,} rows (maximum 500).")
                st.dataframe(result, use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(str(exc))
        st.caption("Mutation statements are blocked to keep the public demo safe and reproducible.")

elif page == "Live Demo Lab":
    hero("Live Demo Lab", "Create session-only transactions and watch dashboard KPIs update without changing the repository database.", eyebrow="Interactive recruiter demo")
    customers, products = get_entities()
    base_facts = get_facts(dims["min_date"], dims["max_date"], (), ())
    if "demo_orders" not in st.session_state:
        st.session_state.demo_orders = []

    def add_event(customer_row, product_row, quantity):
        new_order_id = 900000 + len(st.session_state.demo_orders) + 1
        event = {
            "order_id": new_order_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_id": int(customer_row.customer_id),
            "customer_name": customer_row.customer_name,
            "state": customer_row.state,
            "product_id": int(product_row.product_id),
            "product_name": product_row.product_name,
            "category": product_row.category,
            "quantity": int(quantity),
            "unit_price": float(product_row.list_price),
            "line_revenue": float(product_row.list_price) * int(quantity),
        }
        st.session_state.demo_orders.insert(0, event)

    c1, c2, c3 = st.columns([1.2, 1.2, .6])
    customer_name = c1.selectbox("Customer", customers["customer_name"].tolist())
    product_name = c2.selectbox("Product", products["product_name"].tolist())
    quantity = c3.number_input("Quantity", min_value=1, max_value=20, value=1)
    customer_row = customers.loc[customers["customer_name"] == customer_name].iloc[0]
    product_row = products.loc[products["product_name"] == product_name].iloc[0]
    b1, b2, b3 = st.columns([1, 1, 3])
    if b1.button("Add demo order", type="primary"):
        add_event(customer_row, product_row, quantity)
        st.success("Session-only order added.")
    if b2.button("Generate random order"):
        add_event(customers.sample(1, random_state=random.randint(1, 999999)).iloc[0], products.sample(1, random_state=random.randint(1, 999999)).iloc[0], random.randint(1, 5))
        st.success("Random session-only order generated.")
    if b3.button("Reset live session"):
        st.session_state.demo_orders = []
        st.rerun()

    demo_df = pd.DataFrame(st.session_state.demo_orders)
    base = kpis(base_facts)
    demo_sales = float(demo_df["line_revenue"].sum()) if not demo_df.empty else 0.0
    demo_orders = len(demo_df)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Base sales", money(base["sales"]))
    m2.metric("Live demo sales", money(demo_sales), delta=f"{demo_orders} session orders")
    m3.metric("Combined sales", money(base["sales"] + demo_sales))
    m4.metric("Live conversion", "100%", help="Every generated demo event is treated as a completed order.")

    st.markdown("### Live event feed")
    if demo_df.empty:
        st.info("Add or generate an order to start the live feed.")
    else:
        st.dataframe(demo_df, use_container_width=True, hide_index=True, column_config={"line_revenue": st.column_config.NumberColumn(format="$%.2f"), "unit_price": st.column_config.NumberColumn(format="$%.2f")})
        live_products = demo_df.groupby("product_name", as_index=False)["line_revenue"].sum().sort_values("line_revenue")
        fig = px.bar(live_products, x="line_revenue", y="product_name", orientation="h", title="Live session product sales")
        st.plotly_chart(base_chart_layout(fig), use_container_width=True)

elif page == "Project Guide":
    hero("Project Guide", "Use this section as a presentation script for recruiters, instructors, or teammates.")
    st.markdown("""
### 60-second explanation
RetailPulse is a modernized customer-order analytics platform. The original work used SQL Server, Python, pandas, matplotlib, and seaborn to create a normalized database, insert records, and visualize customer and state sales. I converted that academic workflow into a deployable portfolio product with a five-table 3NF model, SQLite for frictionless cloud hosting, a SQL Server reference implementation, reusable analytical views, a Streamlit dashboard, customer and salesperson drilldowns, a safe SQL explorer, automated tests, CI, and a GitHub Pages overview site.

### Technical flow
1. **Ingest:** Source SQL and notebooks define the entities, records, and original analysis.
2. **Model:** Salesperson → Customer → Order → Order Item, with Product as a reusable dimension.
3. **Transform:** `vw_sales_facts` creates a reporting-friendly fact view.
4. **Analyze:** pandas calculates KPIs and grouped trends.
5. **Visualize:** Plotly and Streamlit provide interactive exploration.
6. **Deliver:** GitHub hosts the code; Streamlit Community Cloud hosts the live app; GitHub Pages hosts the project overview.

### Suggested demo sequence
Open **Overview**, explain the source-to-product modernization, move to **Executive Dashboard**, filter a state, open **Customer 360**, run a query in **Data Explorer**, and finish by generating a transaction in **Live Demo Lab**.
""")
    st.code("streamlit run app.py", language="bash")
    st.caption("Full deployment and GitHub instructions are included in documentation/DEPLOYMENT_GUIDE.md.")
