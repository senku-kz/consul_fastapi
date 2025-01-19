from fastapi import FastAPI
import consul
import uvicorn
import socket
import requests
from typing import Dict

app = FastAPI()

# Consul configuration
CONSUL_HOST = "localhost"
CONSUL_PORT = 8500
SERVICE_NAME = "fastapi-service"
SERVICE_PORT = 8000

# Initialize Consul client
consul_client = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)

def get_host_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def register_service():
    service_id = f"{SERVICE_NAME}-{SERVICE_PORT}"
    
    # Register service with Consul
    consul_client.agent.service.register(
        name=SERVICE_NAME,
        service_id=service_id,
        address=get_host_ip(),
        port=SERVICE_PORT,
        tags=["fastapi", "api"],
        check=consul.Check.http(
            url=f"http://{get_host_ip()}:{SERVICE_PORT}/health",
            interval="10s",
            timeout="5s"
        )
    )
    return service_id

def deregister_service(service_id: str):
    consul_client.agent.service.deregister(service_id)

@app.on_event("startup")
async def startup_event():
    global service_id
    service_id = register_service()

@app.on_event("shutdown")
async def shutdown_event():
    deregister_service(service_id)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI service!"}

@app.get("/services")
async def get_services() -> Dict:
    # Get all services registered in Consul
    services = consul_client.agent.services()
    return services

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT) 