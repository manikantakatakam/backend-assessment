# Backend Developer Technical Assessment

This project implements a data pipeline with three services:
1. **Flask API**: A mock customer data server serving data from a JSON file.
2. **FastAPI**: A data ingestion pipeline that fetches data from the Flask API and stores it in PostgreSQL using the `dlt` library.
3. **PostgreSQL**: A relational database for data storage.

## Project Structure

```
project-root/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── models/customer.py
    ├── services/ingestion.py
    ├── database.py
    ├── Dockerfile
    └── requirements.txt
```

## Getting Started

### Prerequisites
- Docker Desktop
- Python 3.10+
- Git

### Running the Application

1. Start all services using Docker Compose:
   ```bash
   docker-compose up -d --build
   ```

2. Verify the services are running:
   - Flask Mock Server: http://localhost:5000/api/health
   - FastAPI Pipeline: http://localhost:8000/docs

### Testing the Endpoints

1. **Test Flask Mock Server**:
   ```bash
   curl "http://localhost:5000/api/customers?page=1&limit=5"
   ```

2. **Trigger Data Ingestion**:
   ```bash
   curl -X POST http://localhost:8000/api/ingest
   ```

3. **Query Ingested Data**:
   ```bash
   curl "http://localhost:8000/api/customers?page=1&limit=5"
   ```

4. **Get Single Customer**:
   ```bash
   curl "http://localhost:8000/api/customers/CUST001"
   ```

## Implementation Details

- **Flask Mock Server**: Implements pagination and serves data from `data/customers.json`.
- **FastAPI Pipeline**:
  - Uses `SQLAlchemy` for ORM.
  - Uses `dlt` (Data Load Tool) for efficient data ingestion and upsert (merge) logic.
  - Handles auto-pagination when fetching data from the mock server.
- **Docker Compose**: Orchestrates the services and ensures healthy startup order.
"# backend-assessment" 
