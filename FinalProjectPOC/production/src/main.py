#!/usr/bin/env python3
"""
Production application for PostgreSQL to StarRocks real-time data sync using Flink CDC.
This includes comprehensive monitoring, error handling, and production features.
"""

import os
import sys
import asyncio
import signal
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to Python path
sys.path.append(str(Path(__file__).parent))

from production_sync import ProductionSyncApp
from config_manager import ProductionConfigManager
from logger_setup import setup_production_logging
from health_checker import HealthChecker
from metrics_collector import MetricsCollector
from error_handler import ErrorHandler

logger = logging.getLogger(__name__)


class ProductionApp:
    """Main production application class."""
    
    def __init__(self):
        """Initialize the production application."""
        self.sync_app: Optional[ProductionSyncApp] = None
        self.health_checker: Optional[HealthChecker] = None
        self.metrics_collector: Optional[MetricsCollector] = None
        self.error_handler: Optional[ErrorHandler] = None
        self.running = False
        
    async def initialize(self) -> None:
        """Initialize all components."""
        try:
            # Setup logging
            setup_production_logging()
            logger.info("Starting Production PostgreSQL to StarRocks Sync")
            
            # Initialize configuration
            config_manager = ProductionConfigManager()
            logger.info("Configuration loaded successfully")
            
            # Initialize error handler
            self.error_handler = ErrorHandler(config_manager)
            
            # Initialize metrics collector
            self.metrics_collector = MetricsCollector(config_manager)
            await self.metrics_collector.start()
            
            # Initialize health checker
            self.health_checker = HealthChecker(config_manager, self.metrics_collector)
            await self.health_checker.start()
            
            # Initialize sync application
            self.sync_app = ProductionSyncApp(
                config_manager, 
                self.metrics_collector, 
                self.error_handler
            )
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}", exc_info=True)
            raise
    
    async def start(self) -> None:
        """Start the production application."""
        try:
            await self.initialize()
            
            # Start sync application
            await self.sync_app.start()
            
            self.running = True
            logger.info("Production sync application started successfully")
            
            # Setup signal handlers
            self._setup_signal_handlers()
            
            # Keep running until interrupted
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Application failed with error: {e}", exc_info=True)
            await self.shutdown()
            sys.exit(1)
    
    async def shutdown(self) -> None:
        """Gracefully shutdown the application."""
        logger.info("Shutting down production application...")
        self.running = False
        
        try:
            if self.sync_app:
                await self.sync_app.stop()
            
            if self.health_checker:
                await self.health_checker.stop()
            
            if self.metrics_collector:
                await self.metrics_collector.stop()
                
            logger.info("Application shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}", exc_info=True)
    
    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating shutdown...")
            asyncio.create_task(self.shutdown())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Main entry point for the production application."""
    app = ProductionApp()
    await app.start()


if __name__ == "__main__":
    asyncio.run(main())
