from fastapi import FastAPI

from services.api_gateway.routes import events, units, dispatches
from services.shared.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Distributed Disaster Control System - API Gateway")

app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(units.router, prefix="/units", tags=["units"])
app.include_router(dispatches.router, prefix="/dispatches", tags=["dispatches"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "api-gateway"}
