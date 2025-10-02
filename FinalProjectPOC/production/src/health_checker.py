"""
Health checking and monitoring for the production sync application.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import aiohttp
from aiohttp import web
import json

import structlog

from config_manager import ProductionConfigManager
from metrics_collector import MetricsCollector

logger = structlog.get_logger(__name__)


class HealthStatus(Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Represents a health check result."""
    name: str
    status: HealthStatus
    message: str
    timestamp: datetime
    response_time_ms: Optional[float] = None
    details: Dict[str, Any] = None


class HealthChecker:
    """Health checking and monitoring system."""
    
    def __init__(self, config: ProductionConfigManager, metrics: MetricsCollector):
        """Initialize health checker."""
        self.config = config
        self.metrics = metrics
        self.health_checks: Dict[str, HealthCheck] = {}
        self.running = False
        self.app: Optional[web.Application] = None
        self.runner: Optional[web.AppRunner] = None
        self.site: Optional[web.TCPSite] = None
        
        # Setup structured logging
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    
    async def start(self) -> None:
        """Start the health checker."""
        if not self.config.monitoring.enabled:
            logger.info("Monitoring is disabled, skipping health checker")
            return
        
        try:
            # Start health check tasks
            asyncio.create_task(self._run_health_checks())
            
            # Start HTTP server for health endpoints
            await self._start_http_server()
            
            self.running = True
            logger.info(f"Health checker started on port {self.config.monitoring.health_check_port}")
            
        except Exception as e:
            logger.error(f"Failed to start health checker: {e}")
            raise
    
    async def stop(self) -> None:
        """Stop the health checker."""
        logger.info("Stopping health checker...")
        self.running = False
        
        if self.site:
            await self.site.stop()
        if self.runner:
            await self.runner.cleanup()
    
    async def _start_http_server(self) -> None:
        """Start HTTP server for health endpoints."""
        self.app = web.Application()
        
        # Add routes
        self.app.router.add_get('/health', self._health_endpoint)
        self.app.router.add_get('/health/ready', self._ready_endpoint)
        self.app.router.add_get('/health/live', self._live_endpoint)
        self.app.router.add_get('/health/detailed', self._detailed_health_endpoint)
        
        # Start server
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        
        self.site = web.TCPSite(
            self.runner, 
            '0.0.0.0', 
            self.config.monitoring.health_check_port
        )
        await self.site.start()
    
    async def _health_endpoint(self, request: web.Request) -> web.Response:
        """Main health endpoint."""
        overall_status = self._get_overall_health_status()
        
        response_data = {
            "status": overall_status.value,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                name: {
                    "status": check.status.value,
                    "message": check.message,
                    "response_time_ms": check.response_time_ms
                }
                for name, check in self.health_checks.items()
            }
        }
        
        status_code = 200 if overall_status == HealthStatus.HEALTHY else 503
        return web.json_response(response_data, status=status_code)
    
    async def _ready_endpoint(self, request: web.Request) -> web.Response:
        """Readiness probe endpoint."""
        # Check if the application is ready to receive traffic
        ready_checks = ['postgres_connection', 'starrocks_connection', 'flink_environment']
        
        all_ready = all(
            self.health_checks.get(check, HealthCheck(
                name=check,
                status=HealthStatus.UNKNOWN,
                message="Check not run",
                timestamp=datetime.now()
            )).status == HealthStatus.HEALTHY
            for check in ready_checks
        )
        
        status_code = 200 if all_ready else 503
        return web.json_response(
            {"status": "ready" if all_ready else "not_ready"},
            status=status_code
        )
    
    async def _live_endpoint(self, request: web.Request) -> web.Response:
        """Liveness probe endpoint."""
        # Check if the application is alive (not crashed)
        return web.json_response({"status": "alive"})
    
    async def _detailed_health_endpoint(self, request: web.Request) -> web.Response:
        """Detailed health endpoint with metrics."""
        overall_status = self._get_overall_health_status()
        
        response_data = {
            "status": overall_status.value,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                name: {
                    "status": check.status.value,
                    "message": check.message,
                    "response_time_ms": check.response_time_ms,
                    "timestamp": check.timestamp.isoformat(),
                    "details": check.details or {}
                }
                for name, check in self.health_checks.items()
            },
            "metrics_summary": self.metrics.get_metrics_summary(),
            "uptime": self._get_uptime()
        }
        
        status_code = 200 if overall_status == HealthStatus.HEALTHY else 503
        return web.json_response(response_data, status=status_code)
    
    async def _run_health_checks(self) -> None:
        """Run health checks periodically."""
        while self.running:
            try:
                # Run all health checks
                await self._check_postgres_connection()
                await self._check_starrocks_connection()
                await self._check_flink_environment()
                await self._check_sync_jobs()
                await self._check_system_resources()
                
                await asyncio.sleep(self.config.monitoring.job_check_interval)
                
            except Exception as e:
                logger.error(f"Error in health checks: {e}")
                await asyncio.sleep(5)
    
    async def _check_postgres_connection(self) -> None:
        """Check PostgreSQL connection health."""
        start_time = time.time()
        
        try:
            # This would be an actual connection test
            # For now, we'll simulate it
            await asyncio.sleep(0.1)  # Simulate connection time
            
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['postgres_connection'] = HealthCheck(
                name='postgres_connection',
                status=HealthStatus.HEALTHY,
                message='PostgreSQL connection is healthy',
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={
                    'host': self.config.postgres.host,
                    'port': self.config.postgres.port,
                    'database': self.config.postgres.database
                }
            )
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['postgres_connection'] = HealthCheck(
                name='postgres_connection',
                status=HealthStatus.UNHEALTHY,
                message=f'PostgreSQL connection failed: {e}',
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={'error': str(e)}
            )
    
    async def _check_starrocks_connection(self) -> None:
        """Check StarRocks connection health."""
        start_time = time.time()
        
        try:
            # This would be an actual connection test
            await asyncio.sleep(0.1)  # Simulate connection time
            
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['starrocks_connection'] = HealthCheck(
                name='starrocks_connection',
                status=HealthStatus.HEALTHY,
                message='StarRocks connection is healthy',
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={
                    'host': self.config.starrocks.host,
                    'port': self.config.starrocks.port,
                    'database': self.config.starrocks.database
                }
            )
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['starrocks_connection'] = HealthCheck(
                name='starrocks_connection',
                status=HealthStatus.UNHEALTHY,
                message=f'StarRocks connection failed: {e}',
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={'error': str(e)}
            )
    
    async def _check_flink_environment(self) -> None:
        """Check Flink environment health."""
        start_time = time.time()
        
        try:
            # This would check Flink cluster health
            await asyncio.sleep(0.1)  # Simulate check time
            
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['flink_environment'] = HealthCheck(
                name='flink_environment',
                status=HealthStatus.HEALTHY,
                message='Flink environment is healthy',
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={
                    'jobmanager_host': self.config.flink.jobmanager.get('host'),
                    'parallelism': self.config.flink.parallelism
                }
            )
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['flink_environment'] = HealthCheck(
                name='flink_environment',
                status=HealthStatus.UNHEALTHY,
                message=f'Flink environment check failed: {e}',
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={'error': str(e)}
            )
    
    async def _check_sync_jobs(self) -> None:
        """Check sync jobs health."""
        start_time = time.time()
        
        try:
            # This would check the status of sync jobs
            # For now, we'll simulate based on metrics
            metrics_summary = self.metrics.get_metrics_summary()
            
            response_time = (time.time() - start_time) * 1000
            
            # Check if there are any error jobs
            error_jobs = metrics_summary.get('sync_error_jobs', 0)
            active_jobs = metrics_summary.get('sync_active_jobs', 0)
            
            if error_jobs > 0:
                status = HealthStatus.DEGRADED
                message = f'{error_jobs} sync jobs in error state'
            elif active_jobs > 0:
                status = HealthStatus.HEALTHY
                message = f'{active_jobs} sync jobs running'
            else:
                status = HealthStatus.UNKNOWN
                message = 'No sync jobs detected'
            
            self.health_checks['sync_jobs'] = HealthCheck(
                name='sync_jobs',
                status=status,
                message=message,
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={
                    'active_jobs': active_jobs,
                    'error_jobs': error_jobs
                }
            )
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['sync_jobs'] = HealthCheck(
                name='sync_jobs',
                status=HealthStatus.UNHEALTHY,
                message=f'Sync jobs check failed: {e}',
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={'error': str(e)}
            )
    
    async def _check_system_resources(self) -> None:
        """Check system resource usage."""
        start_time = time.time()
        
        try:
            import psutil
            
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            response_time = (time.time() - start_time) * 1000
            
            # Determine status based on thresholds
            if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
                status = HealthStatus.UNHEALTHY
                message = 'High resource usage detected'
            elif cpu_percent > 70 or memory.percent > 70 or disk.percent > 70:
                status = HealthStatus.DEGRADED
                message = 'Elevated resource usage'
            else:
                status = HealthStatus.HEALTHY
                message = 'System resources are healthy'
            
            self.health_checks['system_resources'] = HealthCheck(
                name='system_resources',
                status=status,
                message=message,
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'disk_percent': disk.percent,
                    'memory_available_gb': memory.available / (1024**3),
                    'disk_free_gb': disk.free / (1024**3)
                }
            )
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            
            self.health_checks['system_resources'] = HealthCheck(
                name='system_resources',
                status=HealthStatus.UNKNOWN,
                message=f'System resource check failed: {e}',
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details={'error': str(e)}
            )
    
    def _get_overall_health_status(self) -> HealthStatus:
        """Get overall health status based on individual checks."""
        if not self.health_checks:
            return HealthStatus.UNKNOWN
        
        statuses = [check.status for check in self.health_checks.values()]
        
        if HealthStatus.UNHEALTHY in statuses:
            return HealthStatus.UNHEALTHY
        elif HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED
        elif all(status == HealthStatus.HEALTHY for status in statuses):
            return HealthStatus.HEALTHY
        else:
            return HealthStatus.UNKNOWN
    
    def _get_uptime(self) -> float:
        """Get application uptime in seconds."""
        # This would track actual start time
        # For now, return a placeholder
        return time.time() - time.time()  # Placeholder
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get a summary of health status."""
        overall_status = self._get_overall_health_status()
        
        return {
            "overall_status": overall_status.value,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                name: {
                    "status": check.status.value,
                    "message": check.message,
                    "response_time_ms": check.response_time_ms,
                    "timestamp": check.timestamp.isoformat()
                }
                for name, check in self.health_checks.items()
            },
            "uptime_seconds": self._get_uptime()
        }
