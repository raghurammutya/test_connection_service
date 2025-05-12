from fastapi import FastAPI
from shared_architecture.connections.connection_manager import ConnectionManager
from shared_architecture.utils.health_check_utils import health_check_all
from shared_architecture.utils.logging_utils import init_logging
app = FastAPI(title="Test Connection Service")

@app.on_event("startup")
async def startup_event():
    init_logging("test_connection_service")
    use_mocks = os.getenv("USE_MOCKS", "false").lower() == "true"
    app.state.cm = ConnectionManager("test_connection_service")

    if use_mocks:
        print("🚧 Running with Mocks")
    else:
        print("🚀 Running with Live Connections")
    app.state.cm = ConnectionManager("test_connection_service")
    await app.state.cm.get_redis()
    await app.state.cm.get_mongo()
    await app.state.cm.get_timescaledb()
    await app.state.cm.get_rabbitmq()
    print("✅ All connections initialized successfully.")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/validate")
async def validate_connections():
    checks = await health_check_all()
    return checks
