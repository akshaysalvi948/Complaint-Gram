"""
Configuration management for the demo application.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    """Database configuration model."""
    host: str
    port: int
    database: str
    username: str
    password: str
    schema_name: Optional[str] = "public"


class FlinkConfig(BaseModel):
    """Flink configuration model."""
    jobmanager: Dict[str, Any]
    parallelism: int = 1
    checkpoint_interval: int = 60000
    checkpoint_timeout: int = 300000
    min_pause_between_checkpoints: int = 5000


class TableConfig(BaseModel):
    """Table configuration model."""
    source_table: str
    target_table: str
    primary_key: str
    columns: List[str]


class CDCConfig(BaseModel):
    """CDC configuration model."""
    enabled: bool = True
    snapshot_mode: str = "initial"
    poll_interval_ms: int = 1000
    max_batch_size: int = 1000
    max_wait_time_ms: int = 5000


class LoggingConfig(BaseModel):
    """Logging configuration model."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None


class ConfigManager:
    """Configuration manager for the application."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize configuration manager with config dictionary."""
        self.config = config
        
        # Parse configuration sections
        self.postgres = DatabaseConfig(**config.get('postgres', {}))
        self.starrocks = DatabaseConfig(**config.get('starrocks', {}))
        self.flink = FlinkConfig(**config.get('flink', {}))
        self.tables = [TableConfig(**table) for table in config.get('tables', [])]
        self.cdc = CDCConfig(**config.get('cdc', {}))
        self.logging = LoggingConfig(**config.get('logging', {}))
    
    def get_postgres_connection_string(self) -> str:
        """Get PostgreSQL connection string."""
        return (f"postgresql://{self.postgres.username}:{self.postgres.password}"
                f"@{self.postgres.host}:{self.postgres.port}/{self.postgres.database}")
    
    def get_starrocks_connection_string(self) -> str:
        """Get StarRocks connection string."""
        return (f"mysql://{self.starrocks.username}:{self.starrocks.password}"
                f"@{self.starrocks.host}:{self.starrocks.port}/{self.starrocks.database}")
    
    def get_table_config(self, table_name: str) -> Optional[TableConfig]:
        """Get configuration for a specific table."""
        for table in self.tables:
            if table.source_table == table_name:
                return table
        return None
    
    def get_all_tables(self) -> List[TableConfig]:
        """Get all table configurations."""
        return self.tables
    
    def is_cdc_enabled(self) -> bool:
        """Check if CDC is enabled."""
        return self.cdc.enabled
    
    def get_flink_properties(self) -> Dict[str, str]:
        """Get Flink properties as a dictionary."""
        return {
            "jobmanager.rpc.address": self.flink.jobmanager.get("host", "localhost"),
            "taskmanager.numberOfTaskSlots": str(self.flink.parallelism),
            "parallelism.default": str(self.flink.parallelism),
            "jobmanager.memory.process.size": "1600m",
            "taskmanager.memory.process.size": "1728m",
            "execution.checkpointing.interval": str(self.flink.checkpoint_interval),
            "execution.checkpointing.timeout": str(self.flink.checkpoint_timeout),
            "execution.checkpointing.min-pause": str(self.flink.min_pause_between_checkpoints),
        }
    
    def get_postgres_config(self) -> DatabaseConfig:
        """Get PostgreSQL configuration."""
        return self.postgres
    
    def get_starrocks_config(self) -> DatabaseConfig:
        """Get StarRocks configuration."""
        return self.starrocks
