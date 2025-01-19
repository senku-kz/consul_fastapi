import consul
import socket
from typing import Dict, Optional
from fastapi import HTTPException
import logging
from app.config import Settings

logger = logging.getLogger(__name__)

class ConsulService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.consul_client = consul.Consul(
            host=settings.CONSUL_HOST,
            port=settings.CONSUL_PORT
        )
        self.service_id: Optional[str] = None

    def get_host_ip(self) -> str:
        """Get the host IP address."""
        try:
            hostname = socket.gethostname()
            logger.info(f"Hostname: {hostname}")
            return socket.gethostbyname(hostname)
        except socket.gaierror as e:
            logger.error(f"Failed to get host IP: {e}")
            raise HTTPException(status_code=500, detail="Failed to get host IP")

    def register_service(self) -> str:
        """Register service with Consul."""
        try:
            service_id = f"{self.settings.SERVICE_NAME}-{self.settings.SERVICE_PORT}"
            self.consul_client.agent.service.register(
                name=self.settings.SERVICE_NAME,
                service_id=service_id,
                address=self.get_host_ip(),
                port=self.settings.SERVICE_PORT,
                tags=["fastapi", "api"],
                check=consul.Check.http(
                    url=f"http://{self.get_host_ip()}:{self.settings.SERVICE_PORT}/health",
                    interval="10s",
                    timeout="5s"
                )
            )
            self.service_id = service_id
            logger.info(f"Service registered with ID: {service_id}")
            return service_id
        except Exception as e:
            logger.error(f"Failed to register service: {e}")
            raise HTTPException(status_code=500, detail="Failed to register service")

    def deregister_service(self) -> None:
        """Deregister service from Consul."""
        try:
            if self.service_id:
                self.consul_client.agent.service.deregister(self.service_id)
                logger.info(f"Service deregistered: {self.service_id}")
        except Exception as e:
            logger.error(f"Failed to deregister service: {e}")
            raise HTTPException(status_code=500, detail="Failed to deregister service")

    def get_services(self) -> Dict:
        """Get all registered services."""
        try:
            services = self.consul_client.agent.services()
            return services
        except Exception as e:
            logger.error(f"Failed to get services: {e}")
            raise HTTPException(status_code=500, detail="Failed to get services from Consul") 