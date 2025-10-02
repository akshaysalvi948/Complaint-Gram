"""
Flink CDC Sync implementation for PostgreSQL to StarRocks.
This is the core synchronization logic for the demo.
"""

import logging
import time
from typing import Dict, Any, List, Optional
from pyflink.table import TableEnvironment, EnvironmentSettings
from pyflink.table.descriptors import Schema, OldCsv, FileSystem, ConnectorDescriptor
from pyflink.table.types import DataTypes
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types

from config_manager import ConfigManager, TableConfig

logger = logging.getLogger(__name__)


class FlinkCDCSync:
    """Main class for Flink CDC synchronization."""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize the Flink CDC Sync."""
        self.config = config_manager
        self.env = None
        self.table_env = None
        self.running = False
        
    def _setup_flink_environment(self) -> None:
        """Setup Flink execution environment."""
        try:
            # Create streaming environment
            self.env = StreamExecutionEnvironment.get_execution_environment()
            
            # Set parallelism
            self.env.set_parallelism(self.config.flink.parallelism)
            
            # Enable checkpointing
            self.env.enable_checkpointing(self.config.flink.checkpoint_interval)
            
            # Create table environment
            settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
            self.table_env = TableEnvironment.create(settings)
            
            logger.info("Flink environment setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup Flink environment: {e}")
            raise
    
    def _create_postgres_source_table(self, table_config: TableConfig) -> str:
        """Create PostgreSQL source table in Flink."""
        table_name = f"postgres_{table_config.source_table}"
        
        # Create DDL for PostgreSQL CDC source
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
            'scan.incremental.snapshot.chunk.size' = '8192',
            'scan.snapshot.fetch.size' = '1024',
            'scan.startup.mode' = 'initial'
        )
        """
        
        self.table_env.execute_sql(ddl)
        logger.info(f"Created PostgreSQL source table: {table_name}")
        return table_name
    
    def _create_starrocks_sink_table(self, table_config: TableConfig) -> str:
        """Create StarRocks sink table in Flink."""
        table_name = f"starrocks_{table_config.target_table}"
        
        # Create DDL for StarRocks sink
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
            'sink.buffer-flush.max-rows' = '1000',
            'sink.buffer-flush.interval' = '10s'
        )
        """
        
        self.table_env.execute_sql(ddl)
        logger.info(f"Created StarRocks sink table: {table_name}")
        return table_name
    
    def _get_column_definitions(self, table_config: TableConfig) -> str:
        """Get column definitions for table DDL."""
        # This is a simplified version - in production, you'd want to
        # dynamically determine column types from the source schema
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
    
    def _create_sync_job(self, table_config: TableConfig) -> None:
        """Create synchronization job for a table."""
        try:
            # Create source and sink tables
            source_table = self._create_postgres_source_table(table_config)
            sink_table = self._create_starrocks_sink_table(table_config)
            
            # Create sync query
            sync_query = f"""
            INSERT INTO {sink_table}
            SELECT * FROM {source_table}
            """
            
            # Execute the sync job
            self.table_env.execute_sql(sync_query)
            logger.info(f"Created sync job for table: {table_config.source_table}")
            
        except Exception as e:
            logger.error(f"Failed to create sync job for {table_config.source_table}: {e}")
            raise
    
    def start(self) -> None:
        """Start the synchronization process."""
        try:
            logger.info("Starting Flink CDC synchronization...")
            
            # Setup Flink environment
            self._setup_flink_environment()
            
            # Create sync jobs for all tables
            for table_config in self.config.get_all_tables():
                self._create_sync_job(table_config)
            
            self.running = True
            logger.info("Flink CDC synchronization started successfully")
            
            # Keep the application running
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Failed to start synchronization: {e}")
            raise
    
    def stop(self) -> None:
        """Stop the synchronization process."""
        logger.info("Stopping Flink CDC synchronization...")
        self.running = False
        
        if self.env:
            try:
                self.env.cancel()
                logger.info("Flink job cancelled successfully")
            except Exception as e:
                logger.error(f"Error cancelling Flink job: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current synchronization status."""
        return {
            "running": self.running,
            "tables": [table.source_table for table in self.config.get_all_tables()],
            "flink_parallelism": self.config.flink.parallelism,
            "checkpoint_interval": self.config.flink.checkpoint_interval
        }
