import requests
import dlt
from sqlalchemy.orm import Session
from models.customer import Customer
import os

MOCK_SERVER_URL = os.getenv("MOCK_SERVER_URL", "http://mock-server:5000")

def fetch_all_customers():
    all_customers = []
    page = 1
    limit = 10

    while True:
        response = requests.get(f"{MOCK_SERVER_URL}/api/customers", params={"page": page, "limit": limit})
        if response.status_code != 200:
            break

        data = response.json()
        customers = data.get("data", [])
        if not customers:
            break

        all_customers.extend(customers)

        if len(all_customers) >= data.get("total", 0):
            break

        page += 1

    return all_customers

def run_ingestion():
    customers_data = fetch_all_customers()

    if not customers_data:
        return 0

    # Using dlt for ingestion
    # We change the pipeline name to force a fresh state and avoid schema conflicts
    # We use 'public' dataset name so SQLAlchemy can find the table
    pipeline = dlt.pipeline(
        pipeline_name="customer_ingestion_v3",
        destination="postgres",
        dataset_name="public"
    )

    # dlt handles upserts automatically if we specify primary_key
    # We use 'merge' for upsert logic
    info = pipeline.run(
        dlt.resource(customers_data, name="customers", primary_key="customer_id"),
        write_disposition="merge",
    )

    return len(customers_data)
