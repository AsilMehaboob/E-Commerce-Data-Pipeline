import os
from contextlib import contextmanager
from typing import Generator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from databricks import sql


# Load backend/.env regardless of where the application is started from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


app = FastAPI(
    title="E-Commerce Data API",
    description="API for querying Gold-layer e-commerce analytics",
    version="1.0.0",
)


@contextmanager
def get_connection() -> Generator:
    connection = None

    try:
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            auth_type="databricks-oauth",
        )
        yield connection

    finally:
        if connection is not None:
            connection.close()


def execute_query(query: str):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)

                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()

                return [
                    dict(zip(columns, row))
                    for row in rows
                ]

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Database query failed: {str(exc)}",
        )


@app.get("/")
def root():
    return {
        "message": "E-Commerce Data API is running"
    }


@app.get("/sales/summary")
def sales_summary():
    query = """
        SELECT
            total_orders,
            total_items_sold,
            total_product_revenue,
            total_freight,
            total_revenue,
            average_order_value
        FROM workspace.default.gold_sales_summary
    """

    results = execute_query(query)

    return results[0] if results else {}


@app.get("/products/top")
def top_products():
    query = """
        SELECT
            product_id,
            category_name_english,
            total_revenue,
            total_items_sold
        FROM workspace.default.gold_product_metrics
        ORDER BY total_revenue DESC
        LIMIT 10
    """

    return execute_query(query)


@app.get("/delivery/metrics")
def delivery_metrics():
    query = """
        SELECT
            delivered_orders,
            average_delivery_days,
            minimum_delivery_days,
            maximum_delivery_days,
            average_delivery_delay_days,
            late_orders,
            on_time_orders
        FROM workspace.default.gold_delivery_metrics
    """

    results = execute_query(query)

    return results[0] if results else {}


@app.get("/customers/{customer_id}/metrics")
def customer_metrics(customer_id: str):
    query = f"""
        SELECT
            customer_id,
            total_orders,
            total_items,
            total_product_spend,
            total_freight_spend,
            total_spend,
            average_item_value,
            first_purchase_timestamp,
            last_purchase_timestamp
        FROM workspace.default.gold_customer_metrics
        WHERE customer_id = '{customer_id}'
    """

    results = execute_query(query)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return results[0]