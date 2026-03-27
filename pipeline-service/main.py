from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models.customer import Customer
from services.ingestion import run_ingestion
import uvicorn

# Create tables - we let dlt manage the schema during ingestion
# Base.metadata.create_all(bind=engine)
print("Database table creation via SQLAlchemy is DISABLED. dlt will manage the schema.")

app = FastAPI(title="Data Ingestion Pipeline")

@app.post("/api/ingest")
def ingest_data():
    try:
        records_processed = run_ingestion()
        return {"status": "success", "records_processed": records_processed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers")
def get_customers(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        db: Session = Depends(get_db)
):
    try:
        skip = (page - 1) * limit
        customers = db.query(Customer).offset(skip).limit(limit).all()
        total = db.query(Customer).count()

        return {
            "data": customers,
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        # If table doesn't exist yet, return empty data instead of 500
        if "does not exist" in str(e).lower():
            return {
                "data": [],
                "total": 0,
                "page": page,
                "limit": limit,
                "message": "No data ingested yet. Please run POST /api/ingest first."
            }
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers/{id}")
def get_customer(id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
