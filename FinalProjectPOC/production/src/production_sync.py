"""
Production sync application with comprehensive monitoring and error handling.
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

from pyflink.table import TableEnvironment, EnvironmentSettings
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.typeinfo import Types
from pyflink.common.serialization import SimpleStringSchema

from config_manager import ProductionConfigManager, TableConfig
from metrics_collector import MetricsCollector
from error_handler import ErrorHandler, SyncError, RetryableError

logger = logging.getLogger(__name__)


class SyncStatus(Enum):
    """Synchronization status enumeration."""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"
    STOPPING = "stopping"


@dataclass
class SyncJob:
    """Represents a synchronization job."""
    table_config: TableConfig
    status: SyncStatus
    start_time: Optional[float] = None
    last_checkpoint: Optional[float] = None
    error_count: int = 0
    last_error: Optional[str] = None


class ProductionSyncApp:
    """Production synchronization application with monitoring and error handling."""
    
    def __init__(
        self, 
        config_manager: ProductionConfigManager,
        metrics_collector: MetricsCollector,
        error_handler: ErrorHandler
    ):
        """Initialize the production sync application."""
        self.config = config_manager
        self.metrics = metrics_collector
        self.error_handler = error_handler
        
        self.env: Optional[StreamExecutionEnvironment] = None
        self.table_env: Optional[TableEnvironment] = None
        self.sync_jobs: Dict[str, SyncJob] = {}
        self.running = False
        
    async def start(self) -> None:
        """Start the synchronization application."""
        try:
            logger.info("Starting production sync application...")
            
            # Setup Flink environment
            await self._setup_flink_environment()
            
            # Initialize sync jobs
            await self._initialize_sync_jobs()
            
            # Start monitoring tasks
            asyncio.create_task(self._monitor_jobs())
            asyncio.create_task(self._collect_metrics())
            
            self.running = True
            logger.info("Production sync application started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start sync application: {e}", exc_info=True)
            await self.error_handler.handle_error(e, "sync_startup")
            raise
    
    async def stop(self) -> None:
        """Stop the synchronization application."""
        logger.info("Stopping production sync application...")
        self.running = False
        
        try:
            # Stop all sync jobs
            for job in self.sync_jobs.values():
                await self._stop_sync_job(job)
            
            # Cancel Flink environment
            if self.env:
                self.env.cancel()
            
            logger.info("Production sync application stopped")
            
        except Exception as e:
            logger.error(f"Error stopping sync application: {e}", exc_info=True)
    
    async def _setup_flink_environment(self) -> None:
        """Setup Flink execution environment with production settings."""
        try:
            # Create streaming environment
            self.env = StreamExecutionEnvironment.get_execution_environment()
            
            # Set parallelism
            self.env.set_parallelism(self.config.flink.parallelism)
            
            # Enable checkpointing with production settings
            self.env.enable_checkpointing(self.config.flink.checkpoint_interval)
            
            # Configure checkpointing
            checkpoint_config = self.env.get_checkpoint_config()
            checkpoint_config.set_checkpointing_mode(
                self.config.flink.checkpointing_mode
            )
            checkpoint_config.set_checkpoint_timeout(
                self.config.flink.checkpoint_timeout
            )
            checkpoint_config.set_min_pause_between_checkpoints(
                self.config.flink.min_pause_between_checkpoints
            )
            checkpoint_config.set_max_concurrent_checkpoints(
                self.config.flink.max_concurrent_checkpoints
            )
            
            # Create table environment
            settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
            self.table_env = TableEnvironment.create(settings)
            
            logger.info("Flink environment setup completed with production settings")
            
        except Exception as e:
            logger.error(f"Failed to setup Flink environment: {e}")
            raise
    
    async def _initialize_sync_jobs(self) -> None:
        """Initialize all synchronization jobs."""
        for table_config in self.config.get_all_tables():
            try:
                job = SyncJob(
                    table_config=table_config,
                    status=SyncStatus.STOPPED
                )
                self.sync_jobs[table_config.source_table] = job
                
                # Start the job
                await self._start_sync_job(job)
                
            except Exception as e:
                logger.error(f"Failed to initialize sync job for {table_config.source_table}: {e}")
                await self.error_handler.handle_error(e, f"job_init_{table_config.source_table}")
    
    async def _start_sync_job(self, job: SyncJob) -> None:
        """Start a synchronization job."""
        try:
            job.status = SyncStatus.STARTING
            job.start_time = time.time()
            
            logger.info(f"Starting sync job for table: {job.table_config.source_table}")
            
            # Create source and sink tables
            source_table = await self._create_postgres_source_table(job.table_config)
            sink_table = await self._create_starrocks_sink_table(job.table_config)
            
            # Create and execute sync query
            await self._execute_sync_query(source_table, sink_table, job.table_config)
            
            job.status = SyncStatus.RUNNING
            logger.info(f"Sync job started successfully for table: {job.table_config.source_table}")
            
        except Exception as e:
            job.status = SyncStatus.ERROR
            job.error_count += 1
            job.last_error = str(e)
            logger.error(f"Failed to start sync job for {job.table_config.source_table}: {e}")
            await self.error_handler.handle_error(e, f"job_start_{job.table_config.source_table}")
    
    async def _stop_sync_job(self, job: SyncJob) -> None:
        """Stop a synchronization job."""
        try:
            job.status = SyncStatus.STOPPING
            logger.info(f"Stopping sync job for table: {job.table_config.source_table}")
            
            # Implementation would cancel the specific Flink job here
            # This is simplified for the example
            
            job.status = SyncStatus.STOPPED
            logger.info(f"Sync job stopped for table: {job.table_config.source_table}")
            
        except Exception as e:
            logger.error(f"Error stopping sync job for {job.table_config.source_table}: {e}")
    
    async def _create_postgres_source_table(self, table_config: TableConfig) -> str:
        """Create PostgreSQL source table with production settings."""
        table_name = f"postgres_{table_config.source_table}"
        
        ddl = f"""
        CREATE TABLE {table_name} (
            {self._get_column_definitions(table_config)}
        ) WITH (
            'connector' = 'postgres-cdc',
            'hostname' = '{self.config.postgres.host}',
            'port' = '{self.config.postgres.port}',
            'username' = '{self.config.postgres.username}',
            'password' = '{self.config.postgres.password}',
            'database-name' = '{self.config.postgres.database}',
            'schema-name' = '{self.config.postgres.schema}',
            'table-name' = '{table_config.source_table}',
            'decoding.plugin.name' = 'pgoutput',
            'slot.name' = 'flink_slot_{table_config.source_table}',
            'publication.name' = 'flink_publication_{table_config.source_table}',
            'publication.autocreate.mode' = 'filtered',
            'scan.incremental.snapshot.enabled' = 'true',
            'scan.incremental.snapshot.chunk.size' = '{self.config.cdc.snapshot_chunk_size}',
            'scan.snapshot.fetch.size' = '{self.config.cdc.snapshot_fetch_size}',
            'scan.startup.mode' = '{self.config.cdc.startup_mode}',
            'heartbeat.interval.ms' = '{self.config.cdc.heartbeat_interval}',
            'connect.timeout' = '{self.config.cdc.connect_timeout}',
            'connection.pool.size' = '{self.config.cdc.connection_pool_size}'
        )
        """
        
        self.table_env.execute_sql(ddl)
        return table_name
    
    async def _create_starrocks_sink_table(self, table_config: TableConfig) -> str:
        """Create StarRocks sink table with production settings."""
        table_name = f"starrocks_{table_config.target_table}"
        
        ddl = f"""
        CREATE TABLE {table_name} (
            {self._get_column_definitions(table_config)}
        ) WITH (
            'connector' = 'starrocks',
            'jdbc-url' = 'jdbc:mysql://{self.config.starrocks.host}:{self.config.starrocks.port}/{self.config.starrocks.database}',
            'load-url' = '{self.config.starrocks.host}:{self.config.starrocks.port}',
            'username' = '{self.config.starrocks.username}',
            'password' = '{self.config.starrocks.password}',
            'database-name' = '{self.config.starrocks.database}',
            'table-name' = '{table_config.target_table}',
            'sink.properties.format' = 'json',
            'sink.properties.strip_outer_array' = 'true',
            'sink.buffer-flush.max-rows' = '{self.config.starrocks.buffer_flush_max_rows}',
            'sink.buffer-flush.interval' = '{self.config.starrocks.buffer_flush_interval}',
            'sink.max-retries' = '{self.config.starrocks.max_retries}',
            'sink.retry-delay' = '{self.config.starrocks.retry_delay}'
        )
        """
        
        self.table_env.execute_sql(ddl)
        return table_name
    
    def _get_column_definitions(self, table_config: TableConfig) -> str:
        """Get column definitions for table DDL."""
        column_definitions = []
        
        for column in table_config.columns:
            if column == table_config.primary_key:
                column_definitions.append(f"{column} BIGINT PRIMARY KEY NOT ENFORCED")
            elif column in ['id', 'user_id']:
                column_definitions.append(f"{column} BIGINT")
            elif column in ['quantity', 'price']:
                column_definitions.append(f"{column} DECIMAL(10,2)")
            elif column in ['created_at', 'updated_at']:
                column_definitions.append(f"{column} TIMESTAMP(3)")
            else:
                column_definitions.append(f"{column} STRING")
        
        return ",\n            ".join(column_definitions)
    
    async def _execute_sync_query(self, source_table: str, sink_table: str, table_config: TableConfig) -> None:
        """Execute the synchronization query."""
        sync_query = f"""
        INSERT INTO {sink_table}
        SELECT * FROM {source_table}
        """
        
        self.table_env.execute_sql(sync_query)
    
    async def _monitor_jobs(self) -> None:
        """Monitor sync jobs for health and errors."""
        while self.running:
            try:
                for job in self.sync_jobs.values():
                    await self._check_job_health(job)
                
                await asyncio.sleep(self.config.monitoring.job_check_interval)
                
            except Exception as e:
                logger.error(f"Error in job monitoring: {e}")
                await asyncio.sleep(5)
    
    async def _check_job_health(self, job: SyncJob) -> None:
        """Check the health of a sync job."""
        try:
            if job.status == SyncStatus.ERROR:
                # Attempt to restart the job
                if job.error_count < self.config.error_handling.max_retries:
                    logger.info(f"Attempting to restart job for {job.table_config.source_table}")
                    await self._start_sync_job(job)
                else:
                    logger.error(f"Job for {job.table_config.source_table} exceeded max retries")
            
            # Update metrics
            await self.metrics.record_job_status(job.table_config.source_table, job.status.value)
            
        except Exception as e:
            logger.error(f"Error checking job health for {job.table_config.source_table}: {e}")
    
    async def _collect_metrics(self) -> None:
        """Collect and record metrics."""
        while self.running:
            try:
                # Record application metrics
                await self.metrics.record_app_metrics({
                    "running_jobs": len([j for j in self.sync_jobs.values() if j.status == SyncStatus.RUNNING]),
                    "error_jobs": len([j for j in self.sync_jobs.values() if j.status == SyncStatus.ERROR]),
                    "total_jobs": len(self.sync_jobs)
                })
                
                await asyncio.sleep(self.config.monitoring.metrics_collection_interval)
                
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
                await asyncio.sleep(5)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current application status."""
        return {
            "running": self.running,
            "jobs": {
                name: {
                    "status": job.status.value,
                    "error_count": job.error_count,
                    "last_error": job.last_error,
                    "uptime": time.time() - job.start_time if job.start_time else 0
                }
                for name, job in self.sync_jobs.items()
            },
            "flink_parallelism": self.config.flink.parallelism,
            "checkpoint_interval": self.config.flink.checkpoint_interval
        }
