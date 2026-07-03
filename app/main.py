from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.entrypoints.api.payment_routes import (
    router as payment_router,
)
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    yield


app = FastAPI(
    title="Payment Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(payment_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )