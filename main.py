from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import uvicorn
import logging
from typing import Dict

from app.config import get_settings, Settings
from app.services.consul_service import ConsulService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize ConsulService
consul_service = ConsulService(get_settings())

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    try:
        # Startup
        consul_service.register_service()
        logger.info("Application startup completed")
        yield
    finally:
        # Shutdown
        consul_service.deregister_service()
        logger.info("Application shutdown completed")

app = FastAPI(
    title="FastAPI Service",
    description="A FastAPI service with Consul integration",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {"message": "Hello from FastAPI service!"}

@app.get("/services", tags=["Services"])
async def get_services(settings: Settings = Depends(get_settings)) -> Dict:
    """Get all services registered in Consul."""
    return consul_service.get_services()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    ) 