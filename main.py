from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import logging
from app.config import get_settings
from app.services.consul_service import ConsulService
from app.api.router import router, consul_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

# Include router
app.include_router(router)

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    ) 