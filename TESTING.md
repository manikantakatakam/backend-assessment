# Testing Guide: Backend Data Pipeline

Follow these steps to verify that the data pipeline is working perfectly.

## 1. Prerequisites Check
Ensure you are in the project root directory:
```bash
cd C:\Users\Manikanta.K\Downloads\backend-data-pipeline-assessment
```

### CRITICAL: Verify Code Content
Before building, open `pipeline-service/main.py` and ensure line 9 is commented out:
```python
# Base.metadata.create_all(bind=engine)
```
If it is NOT commented out, the ingestion will fail.

Verify that the `Dockerfile` exists in both service folders:
```cmd
dir mock-server\Dockerfile
dir pipeline-service\Dockerfile
```

---

## 2. Start the Services
Build and start the containers in detached mode:
```bash
docker-compose up -d --build
```

Check if all 3 services are running:
```bash
docker ps
```
*Expected Output: You should see `postgres:15`, `mock-server`, and `pipeline-service` in the list.*

---

## 3. Test Flask Mock Server (Port 5000)
Verify the source data is being served correctly from the JSON file.

### Health Check
```bash
curl http://localhost:5000/api/health
```
*Expected: `{"status": "healthy"}`*

### Paginated Customers
```bash
curl "http://localhost:5000/api/customers?page=1&limit=5"
```
*Expected: A JSON object with 5 customer records and `total: 21`.*

---

## 4. Test FastAPI Ingestion (Port 8000)
This is the core of the assessment.

### Trigger Ingestion
```bash
curl -X POST http://localhost:8000/api/ingest
```
*Expected: `{"status": "success", "records_processed": 21}`*
*Note: This step fetches data from Flask and saves it to PostgreSQL.*

### Verify Data in Database
Now, query the FastAPI service to see if it returns the data from the database:
```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
```
*Expected: The same 5 records, but this time they are being served from PostgreSQL.*

### Test Single Customer
```bash
curl http://localhost:8000/api/customers/CUST001
```
*Expected: Detailed JSON for John Doe.*

---

## 5. Troubleshooting

### "Dockerfile: no such file or directory"
If you see this error:
1. Check if the file is named `Dockerfile` (no extension).
2. Ensure you are running `docker-compose` from the folder containing `docker-compose.yml`.
3. If you are on Windows, ensure the file isn't actually `Dockerfile.txt`.

### "Failed to connect to localhost port 8000"
This means the FastAPI service didn't start. Check the logs:
```bash
docker-compose logs pipeline-service
```

### Resetting the Environment
If you want to start fresh and clear the database:
```bash
docker-compose down -v
docker-compose up -d --build
```
