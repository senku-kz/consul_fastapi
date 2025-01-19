from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from app.config import Settings, get_settings
from app.services.consul_service import ConsulService

# Create router instance
router = APIRouter()

# Initialize ConsulService
consul_service = ConsulService(get_settings())

@router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@router.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {"message": "Hello from FastAPI service!"}

@router.get("/services", tags=["Services"])
async def get_services(settings: Settings = Depends(get_settings)) -> Dict:
    """Get all services registered in Consul."""
    return consul_service.get_services() 