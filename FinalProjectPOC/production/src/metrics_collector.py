"""
Metrics collection and monitoring for the production sync application.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from prometheus_client import Counter, Histogram, Gauge, start_http_server, CollectorRegistry
import structlog

from config_manager import ProductionConfigManager

logger = structlog.get_logger(__name__)


@dataclass
class MetricData:
    """Represents a metric data point."""
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class MetricsCollector:
    """Collects and exposes metrics for monitoring."""
    
    def __init__(self, config: ProductionConfigManager):
        """Initialize metrics collector."""
        self.config = config
        self.registry = CollectorRegistry()
        self.metrics: Dict[str, Any] = {}
        self.running = False
        self.metrics_buffer: List[MetricData] = []
        
        # Initialize Prometheus metrics
        self._init_prometheus_metrics()
        
        # Setup structured logging
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
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
    
    def _init_prometheus_metrics(self) -> None:
        """Initialize Prometheus metrics."""
        # Counters
        self.metrics['records_processed'] = Counter(
            'sync_records_processed_total',
            'Total number of records processed',
            ['table', 'operation'],
            registry=self.registry
        )
        
        self.metrics['records_failed'] = Counter(
            'sync_records_failed_total',
            'Total number of records that failed to process',
            ['table', 'error_type'],
            registry=self.registry
        )
        
        self.metrics['checkpoints_completed'] = Counter(
            'sync_checkpoints_completed_total',
            'Total number of checkpoints completed',
            ['table'],
            registry=self.registry
        )
        
        self.metrics['checkpoints_failed'] = Counter(
            'sync_checkpoints_failed_total',
            'Total number of checkpoints that failed',
            ['table'],
            registry=self.registry
        )
        
        # Histograms
        self.metrics['processing_latency'] = Histogram(
            'sync_processing_latency_seconds',
            'Processing latency in seconds',
            ['table', 'operation'],
            buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0],
            registry=self.registry
        )
        
        self.metrics['batch_size'] = Histogram(
            'sync_batch_size',
            'Batch size distribution',
            ['table'],
            buckets=[1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000],
            registry=self.registry
        )
        
        # Gauges
        self.metrics['active_jobs'] = Gauge(
            'sync_active_jobs',
            'Number of active sync jobs',
            registry=self.registry
        )
        
        self.metrics['error_jobs'] = Gauge(
            'sync_error_jobs',
            'Number of jobs in error state',
            registry=self.registry
        )
        
        self.metrics['last_checkpoint_time'] = Gauge(
            'sync_last_checkpoint_timestamp_seconds',
            'Timestamp of the last checkpoint',
            ['table'],
            registry=self.registry
        )
        
        self.metrics['throughput'] = Gauge(
            'sync_throughput_records_per_second',
            'Current throughput in records per second',
            ['table'],
            registry=self.registry
        )
        
        self.metrics['lag_seconds'] = Gauge(
            'sync_lag_seconds',
            'Current lag in seconds',
            ['table'],
            registry=self.registry
        )
    
    async def start(self) -> None:
        """Start the metrics collector."""
        if not self.config.monitoring.enabled:
            logger.info("Monitoring is disabled, skipping metrics collection")
            return
        
        try:
            # Start Prometheus HTTP server
            start_http_server(
                self.config.monitoring.metrics_port,
                registry=self.registry
            )
            
            self.running = True
            
            # Start background tasks
            asyncio.create_task(self._process_metrics_buffer())
            asyncio.create_task(self._calculate_derived_metrics())
            
            logger.info(f"Metrics collector started on port {self.config.monitoring.metrics_port}")
            
        except Exception as e:
            logger.error(f"Failed to start metrics collector: {e}")
            raise
    
    async def stop(self) -> None:
        """Stop the metrics collector."""
        logger.info("Stopping metrics collector...")
        self.running = False
    
    async def record_record_processed(self, table: str, operation: str, count: int = 1) -> None:
        """Record a processed record."""
        self.metrics['records_processed'].labels(
            table=table, 
            operation=operation
        ).inc(count)
        
        await self._add_to_buffer(MetricData(
            name="record_processed",
            value=count,
            labels={"table": table, "operation": operation}
        ))
    
    async def record_record_failed(self, table: str, error_type: str, count: int = 1) -> None:
        """Record a failed record."""
        self.metrics['records_failed'].labels(
            table=table, 
            error_type=error_type
        ).inc(count)
        
        await self._add_to_buffer(MetricData(
            name="record_failed",
            value=count,
            labels={"table": table, "error_type": error_type}
        ))
    
    async def record_processing_latency(self, table: str, operation: str, latency: float) -> None:
        """Record processing latency."""
        self.metrics['processing_latency'].labels(
            table=table, 
            operation=operation
        ).observe(latency)
    
    async def record_batch_size(self, table: str, size: int) -> None:
        """Record batch size."""
        self.metrics['batch_size'].labels(table=table).observe(size)
    
    async def record_checkpoint_completed(self, table: str) -> None:
        """Record a completed checkpoint."""
        self.metrics['checkpoints_completed'].labels(table=table).inc()
        self.metrics['last_checkpoint_time'].labels(table=table).set(time.time())
    
    async def record_checkpoint_failed(self, table: str) -> None:
        """Record a failed checkpoint."""
        self.metrics['checkpoints_failed'].labels(table=table).inc()
    
    async def record_job_status(self, table: str, status: str) -> None:
        """Record job status."""
        if status == "running":
            self.metrics['active_jobs'].inc()
        elif status == "error":
            self.metrics['error_jobs'].inc()
    
    async def record_app_metrics(self, metrics: Dict[str, Any]) -> None:
        """Record application-level metrics."""
        for name, value in metrics.items():
            if name in self.metrics:
                if hasattr(self.metrics[name], 'set'):
                    self.metrics[name].set(value)
                elif hasattr(self.metrics[name], 'inc'):
                    self.metrics[name].inc(value)
    
    async def record_throughput(self, table: str, records_per_second: float) -> None:
        """Record throughput for a table."""
        self.metrics['throughput'].labels(table=table).set(records_per_second)
    
    async def record_lag(self, table: str, lag_seconds: float) -> None:
        """Record lag for a table."""
        self.metrics['lag_seconds'].labels(table=table).set(lag_seconds)
    
    async def _add_to_buffer(self, metric: MetricData) -> None:
        """Add metric to buffer for processing."""
        self.metrics_buffer.append(metric)
        
        # Limit buffer size
        if len(self.metrics_buffer) > 10000:
            self.metrics_buffer = self.metrics_buffer[-5000:]
    
    async def _process_metrics_buffer(self) -> None:
        """Process metrics buffer periodically."""
        while self.running:
            try:
                if self.metrics_buffer:
                    # Process buffered metrics
                    processed_count = len(self.metrics_buffer)
                    self.metrics_buffer.clear()
                    
                    logger.debug(f"Processed {processed_count} metrics from buffer")
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing metrics buffer: {e}")
                await asyncio.sleep(5)
    
    async def _calculate_derived_metrics(self) -> None:
        """Calculate derived metrics like throughput and lag."""
        while self.running:
            try:
                # Calculate throughput for each table
                for table_config in self.config.get_all_tables():
                    table = table_config.source_table
                    
                    # This is a simplified calculation
                    # In production, you'd track actual record counts over time
                    current_time = time.time()
                    
                    # Simulate throughput calculation
                    # In real implementation, you'd track actual metrics
                    throughput = 100.0  # Placeholder
                    await self.record_throughput(table, throughput)
                    
                    # Simulate lag calculation
                    lag = 0.0  # Placeholder
                    await self.record_lag(table, lag)
                
                await asyncio.sleep(self.config.monitoring.metrics_collection_interval)
                
            except Exception as e:
                logger.error(f"Error calculating derived metrics: {e}")
                await asyncio.sleep(5)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of current metrics."""
        summary = {}
        
        for name, metric in self.metrics.items():
            try:
                if hasattr(metric, '_value'):
                    summary[name] = metric._value
                elif hasattr(metric, '_sum'):
                    summary[name] = metric._sum
                else:
                    summary[name] = "N/A"
            except Exception as e:
                logger.warning(f"Could not get value for metric {name}: {e}")
                summary[name] = "Error"
        
        return summary
    
    async def export_metrics(self) -> str:
        """Export metrics in Prometheus format."""
        from prometheus_client import generate_latest
        
        try:
            return generate_latest(self.registry).decode('utf-8')
        except Exception as e:
            logger.error(f"Error exporting metrics: {e}")
            return ""
