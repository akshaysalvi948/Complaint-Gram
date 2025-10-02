"""
Production configuration management with advanced features.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from pydantic import BaseModel, Field, validator
import yaml
import os
from pathlib import Path


class DatabaseConfig(BaseModel):
    """Database configuration model."""
    host: str
    port: int
    database: str
    username: str
    password: str
    schema: Optional[str] = "public"
    connection_pool_size: int = 10
    connection_timeout: int = 30
    query_timeout: int = 300


class FlinkConfig(BaseModel):
    """Flink configuration model."""
    jobmanager: Dict[str, Any]
    parallelism: int = 4
    checkpoint_interval: int = 60000
    checkpoint_timeout: int = 300000
    min_pause_between_checkpoints: int = 5000
    max_concurrent_checkpoints: int = 1
    checkpointing_mode: str = "EXACTLY_ONCE"
    restart_strategy: str = "exponential-delay"
    restart_attempts: int = 3
    restart_delay: int = 10000
    restart_max_delay: int = 60000
    restart_backoff_multiplier: float = 2.0


class TableConfig(BaseModel):
    """Table configuration model."""
    source_table: str
    target_table: str
    primary_key: str
    columns: List[str]
    sync_mode: str = "cdc"  # cdc, batch, hybrid
    batch_size: int = 1000
    sync_interval: int = 60  # seconds
    enabled: bool = True


class CDCConfig(BaseModel):
    """CDC configuration model."""
    enabled: bool = True
    startup_mode: str = "initial"  # initial, latest, timestamp
    snapshot_mode: str = "initial"
    poll_interval_ms: int = 1000
    max_batch_size: int = 1000
    max_wait_time_ms: int = 5000
    snapshot_chunk_size: int = 8192
    snapshot_fetch_size: int = 1024
    heartbeat_interval: int = 30000
    connect_timeout: int = 30000
    connection_pool_size: int = 10


class StarRocksConfig(DatabaseConfig):
    """StarRocks specific configuration."""
    buffer_flush_max_rows: int = 1000
    buffer_flush_interval: str = "10s"
    max_retries: int = 3
    retry_delay: int = 1000
    load_timeout: int = 600000


class MonitoringConfig(BaseModel):
    """Monitoring configuration model."""
    enabled: bool = True
    metrics_port: int = 9090
    health_check_port: int = 8080
    job_check_interval: int = 30  # seconds
    metrics_collection_interval: int = 10  # seconds
    alert_thresholds: Dict[str, float] = Field(default_factory=lambda: {
        "error_rate": 0.05,
        "latency_p99": 1000.0,
        "throughput_min": 100.0
    })


class ErrorHandlingConfig(BaseModel):
    """Error handling configuration model."""
    max_retries: int = 3
    retry_delay: int = 5000  # milliseconds
    exponential_backoff: bool = True
    max_retry_delay: int = 300000  # 5 minutes
    dead_letter_queue: bool = True
    alert_on_error: bool = True
    error_notification_webhook: Optional[str] = None


class LoggingConfig(BaseModel):
    """Logging configuration model."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    json_format: bool = False
    structured_logging: bool = True


class SecurityConfig(BaseModel):
    """Security configuration model."""
    enable_ssl: bool = False
    ssl_cert_path: Optional[str] = None
    ssl_key_path: Optional[str] = None
    enable_encryption: bool = False
    encryption_key: Optional[str] = None
    enable_audit_logging: bool = True


class ProductionConfigManager:
    """Production configuration manager with advanced features."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        if config_path is None:
            config_path = os.getenv('CONFIG_PATH', 'config/production_config.yaml')
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # Parse configuration sections
        self.postgres = DatabaseConfig(**self.config.get('postgres', {}))
        self.starrocks = StarRocksConfig(**self.config.get('starrocks', {}))
        self.flink = FlinkConfig(**self.config.get('flink', {}))
        self.tables = [TableConfig(**table) for table in self.config.get('tables', [])]
        self.cdc = CDCConfig(**self.config.get('cdc', {}))
        self.monitoring = MonitoringConfig(**self.config.get('monitoring', {}))
        self.error_handling = ErrorHandlingConfig(**self.config.get('error_handling', {}))
        self.logging = LoggingConfig(**self.config.get('logging', {}))
        self.security = SecurityConfig(**self.config.get('security', {}))
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or environment variables."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
        else:
            # Load from environment variables
            config = self._load_from_env()
        
        return config
    
    def _load_from_env(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        return {
            'postgres': {
                'host': os.getenv('POSTGRES_HOST', 'localhost'),
                'port': int(os.getenv('POSTGRES_PORT', '5432')),
                'database': os.getenv('POSTGRES_DB', 'production_db'),
                'username': os.getenv('POSTGRES_USER', 'postgres'),
                'password': os.getenv('POSTGRES_PASSWORD', 'password'),
                'schema': os.getenv('POSTGRES_SCHEMA', 'public'),
                'connection_pool_size': int(os.getenv('POSTGRES_POOL_SIZE', '10')),
                'connection_timeout': int(os.getenv('POSTGRES_TIMEOUT', '30')),
                'query_timeout': int(os.getenv('POSTGRES_QUERY_TIMEOUT', '300'))
            },
            'starrocks': {
                'host': os.getenv('STARROCKS_HOST', 'localhost'),
                'port': int(os.getenv('STARROCKS_PORT', '8030')),
                'database': os.getenv('STARROCKS_DB', 'production_db'),
                'username': os.getenv('STARROCKS_USER', 'root'),
                'password': os.getenv('STARROCKS_PASSWORD', 'root'),
                'buffer_flush_max_rows': int(os.getenv('STARROCKS_BUFFER_ROWS', '1000')),
                'buffer_flush_interval': os.getenv('STARROCKS_BUFFER_INTERVAL', '10s'),
                'max_retries': int(os.getenv('STARROCKS_MAX_RETRIES', '3')),
                'retry_delay': int(os.getenv('STARROCKS_RETRY_DELAY', '1000')),
                'load_timeout': int(os.getenv('STARROCKS_LOAD_TIMEOUT', '600000'))
            },
            'flink': {
                'jobmanager': {
                    'host': os.getenv('FLINK_JOBMANAGER_HOST', 'localhost'),
                    'port': int(os.getenv('FLINK_JOBMANAGER_PORT', '8081'))
                },
                'parallelism': int(os.getenv('FLINK_PARALLELISM', '4')),
                'checkpoint_interval': int(os.getenv('FLINK_CHECKPOINT_INTERVAL', '60000')),
                'checkpoint_timeout': int(os.getenv('FLINK_CHECKPOINT_TIMEOUT', '300000')),
                'min_pause_between_checkpoints': int(os.getenv('FLINK_MIN_PAUSE', '5000')),
                'max_concurrent_checkpoints': int(os.getenv('FLINK_MAX_CONCURRENT', '1')),
                'checkpointing_mode': os.getenv('FLINK_CHECKPOINT_MODE', 'EXACTLY_ONCE'),
                'restart_strategy': os.getenv('FLINK_RESTART_STRATEGY', 'exponential-delay'),
                'restart_attempts': int(os.getenv('FLINK_RESTART_ATTEMPTS', '3')),
                'restart_delay': int(os.getenv('FLINK_RESTART_DELAY', '10000')),
                'restart_max_delay': int(os.getenv('FLINK_RESTART_MAX_DELAY', '60000')),
                'restart_backoff_multiplier': float(os.getenv('FLINK_RESTART_BACKOFF', '2.0'))
            },
            'tables': self._parse_tables_from_env(),
            'cdc': {
                'enabled': os.getenv('CDC_ENABLED', 'true').lower() == 'true',
                'startup_mode': os.getenv('CDC_STARTUP_MODE', 'initial'),
                'snapshot_mode': os.getenv('CDC_SNAPSHOT_MODE', 'initial'),
                'poll_interval_ms': int(os.getenv('CDC_POLL_INTERVAL', '1000')),
                'max_batch_size': int(os.getenv('CDC_MAX_BATCH_SIZE', '1000')),
                'max_wait_time_ms': int(os.getenv('CDC_MAX_WAIT_TIME', '5000')),
                'snapshot_chunk_size': int(os.getenv('CDC_SNAPSHOT_CHUNK_SIZE', '8192')),
                'snapshot_fetch_size': int(os.getenv('CDC_SNAPSHOT_FETCH_SIZE', '1024')),
                'heartbeat_interval': int(os.getenv('CDC_HEARTBEAT_INTERVAL', '30000')),
                'connect_timeout': int(os.getenv('CDC_CONNECT_TIMEOUT', '30000')),
                'connection_pool_size': int(os.getenv('CDC_CONNECTION_POOL_SIZE', '10'))
            },
            'monitoring': {
                'enabled': os.getenv('MONITORING_ENABLED', 'true').lower() == 'true',
                'metrics_port': int(os.getenv('METRICS_PORT', '9090')),
                'health_check_port': int(os.getenv('HEALTH_CHECK_PORT', '8080')),
                'job_check_interval': int(os.getenv('JOB_CHECK_INTERVAL', '30')),
                'metrics_collection_interval': int(os.getenv('METRICS_COLLECTION_INTERVAL', '10')),
                'alert_thresholds': {
                    'error_rate': float(os.getenv('ALERT_ERROR_RATE', '0.05')),
                    'latency_p99': float(os.getenv('ALERT_LATENCY_P99', '1000.0')),
                    'throughput_min': float(os.getenv('ALERT_THROUGHPUT_MIN', '100.0'))
                }
            },
            'error_handling': {
                'max_retries': int(os.getenv('ERROR_MAX_RETRIES', '3')),
                'retry_delay': int(os.getenv('ERROR_RETRY_DELAY', '5000')),
                'exponential_backoff': os.getenv('ERROR_EXPONENTIAL_BACKOFF', 'true').lower() == 'true',
                'max_retry_delay': int(os.getenv('ERROR_MAX_RETRY_DELAY', '300000')),
                'dead_letter_queue': os.getenv('ERROR_DEAD_LETTER_QUEUE', 'true').lower() == 'true',
                'alert_on_error': os.getenv('ERROR_ALERT_ON_ERROR', 'true').lower() == 'true',
                'error_notification_webhook': os.getenv('ERROR_NOTIFICATION_WEBHOOK')
            },
            'logging': {
                'level': os.getenv('LOG_LEVEL', 'INFO'),
                'format': os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                'file': os.getenv('LOG_FILE'),
                'max_file_size': int(os.getenv('LOG_MAX_FILE_SIZE', str(10 * 1024 * 1024))),
                'backup_count': int(os.getenv('LOG_BACKUP_COUNT', '5')),
                'json_format': os.getenv('LOG_JSON_FORMAT', 'false').lower() == 'true',
                'structured_logging': os.getenv('LOG_STRUCTURED', 'true').lower() == 'true'
            },
            'security': {
                'enable_ssl': os.getenv('SECURITY_ENABLE_SSL', 'false').lower() == 'true',
                'ssl_cert_path': os.getenv('SECURITY_SSL_CERT_PATH'),
                'ssl_key_path': os.getenv('SECURITY_SSL_KEY_PATH'),
                'enable_encryption': os.getenv('SECURITY_ENABLE_ENCRYPTION', 'false').lower() == 'true',
                'encryption_key': os.getenv('SECURITY_ENCRYPTION_KEY'),
                'enable_audit_logging': os.getenv('SECURITY_AUDIT_LOGGING', 'true').lower() == 'true'
            }
        }
    
    def _parse_tables_from_env(self) -> List[Dict[str, Any]]:
        """Parse table configurations from environment variables."""
        tables_env = os.getenv('SYNC_TABLES', '')
        if not tables_env:
            return []
        
        tables = []
        for table_def in tables_env.split(';'):
            if not table_def.strip():
                continue
            
            parts = table_def.split(',')
            if len(parts) >= 3:
                tables.append({
                    'source_table': parts[0].strip(),
                    'target_table': parts[1].strip(),
                    'primary_key': parts[2].strip(),
                    'columns': parts[3].split('|') if len(parts) > 3 else [],
                    'sync_mode': parts[4] if len(parts) > 4 else 'cdc',
                    'batch_size': int(parts[5]) if len(parts) > 5 else 1000,
                    'sync_interval': int(parts[6]) if len(parts) > 6 else 60,
                    'enabled': parts[7].lower() == 'true' if len(parts) > 7 else True
                })
        
        return tables
    
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
        return [table for table in self.tables if table.enabled]
    
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
            "execution.checkpointing.max-concurrent-checkpoints": str(self.flink.max_concurrent_checkpoints),
            "execution.checkpointing.mode": self.flink.checkpointing_mode,
            "restart-strategy": self.flink.restart_strategy,
            "restart-strategy.exponential-delay.attempts": str(self.flink.restart_attempts),
            "restart-strategy.exponential-delay.initial-backoff": str(self.flink.restart_delay),
            "restart-strategy.exponential-delay.max-backoff": str(self.flink.restart_max_delay),
            "restart-strategy.exponential-delay.backoff-multiplier": str(self.flink.restart_backoff_multiplier)
        }
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Validate required fields
        if not self.postgres.host:
            errors.append("PostgreSQL host is required")
        
        if not self.starrocks.host:
            errors.append("StarRocks host is required")
        
        if not self.tables:
            errors.append("At least one table configuration is required")
        
        # Validate table configurations
        for table in self.tables:
            if not table.source_table:
                errors.append(f"Source table name is required for table {table}")
            if not table.target_table:
                errors.append(f"Target table name is required for table {table}")
            if not table.primary_key:
                errors.append(f"Primary key is required for table {table}")
        
        return errors
