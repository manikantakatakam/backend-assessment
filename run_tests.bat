@echo off
SETLOCAL EnableDelayedExpansion

echo ============================================================
echo   BACKEND DATA PIPELINE - AUTOMATED TEST SUITE
echo ============================================================

:: 1. Check for docker-compose.yml
if not exist "docker-compose.yml" (
    echo [ERROR] docker-compose.yml not found in current directory.
    echo Please run this script from the project root.
    exit /b 1
)

:: 2. Clean up existing environment
echo [1/5] Cleaning up old environment (wiping database)...
docker compose down -v >nul 2>&1
echo [OK] Environment cleaned.

:: 3. Build and Start Services
echo [2/5] Building and starting services (this may take a minute)...
docker compose up -d --build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker Compose failed to start.
    exit /b 1
)

:: 4. Wait for services to be healthy
echo [3/5] Waiting for services to initialize...
echo (Waiting 15 seconds for Postgres health check and service startup)
timeout /t 15 /nobreak >nul

:: 5. Test Flask Mock Server
echo [4/5] Testing Flask Mock Server (Port 5000)...
curl -s http://localhost:5000/api/health | findstr "healthy" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Flask Mock Server is healthy.
) else (
    echo [ERROR] Flask Mock Server is not responding correctly.
    docker compose logs mock-server
    exit /b 1
)

:: 6. Trigger FastAPI Ingestion
echo [5/5] Triggering FastAPI Ingestion (Port 8000)...
echo Sending POST request to /api/ingest...
for /f "tokens=*" %%i in ('curl -s -X POST http://localhost:8000/api/ingest') do set RESPONSE=%%i

echo Response: !RESPONSE!

echo !RESPONSE! | findstr "success" >nul
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Data ingestion completed perfectly!
) else (
    echo [ERROR] Ingestion failed. See response above.
    echo Checking pipeline-service logs:
    docker compose logs pipeline-service
    exit /b 1
)

:: 7. Final Verification
echo.
echo ============================================================
echo   VERIFICATION SUMMARY
echo ============================================================
echo Querying database for first 2 customers:
curl -s "http://localhost:8000/api/customers?limit=2"
echo.
echo ============================================================
echo   TESTS COMPLETED SUCCESSFULLY
echo ============================================================

pause
