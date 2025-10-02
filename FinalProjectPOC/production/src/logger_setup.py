"""
Production logging setup with structured logging and advanced features.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import structlog
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in {
                'name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                'filename', 'module', 'exc_info', 'exc_text', 'stack_info',
                'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
                'thread', 'threadName', 'processName', 'process', 'getMessage'
            }:
                log_entry[key] = value
        
        return json.dumps(log_entry, default=str)


def setup_production_logging(
    level: str = "INFO",
    log_format: Optional[str] = None,
    log_file: Optional[str] = None,
    json_format: bool = True,
    structured_logging: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """
    Setup production logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string
        log_file: Path to log file (optional)
        json_format: Use JSON formatting for logs
        structured_logging: Enable structured logging with structlog
        max_file_size: Maximum log file size in bytes
        backup_count: Number of backup files to keep
    """
    # Configure structlog if enabled
    if structured_logging:
        _setup_structlog(level, json_format)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        if log_format is None:
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger("pyflink").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    # Configure specific loggers for better control
    _configure_specific_loggers(level)


def _setup_structlog(level: str, json_format: bool) -> None:
    """Setup structlog configuration."""
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    if json_format:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def _configure_specific_loggers(level: str) -> None:
    """Configure specific loggers with appropriate levels."""
    logger_configs = {
        "postgres_starrocks_sync": level,
        "flink_cdc_sync": level,
        "metrics_collector": level,
        "error_handler": level,
        "health_checker": level,
        "config_manager": level,
        "production_sync": level,
    }
    
    for logger_name, log_level in logger_configs.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, log_level.upper()))


class ContextualLogger:
    """Contextual logger that adds context to log messages."""
    
    def __init__(self, name: str, context: Optional[Dict[str, Any]] = None):
        """Initialize contextual logger."""
        self.logger = structlog.get_logger(name)
        self.context = context or {}
    
    def bind(self, **kwargs) -> 'ContextualLogger':
        """Bind additional context to the logger."""
        new_context = {**self.context, **kwargs}
        return ContextualLogger(self.logger.name, new_context)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with context."""
        self.logger.debug(message, **{**self.context, **kwargs})
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message with context."""
        self.logger.info(message, **{**self.context, **kwargs})
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with context."""
        self.logger.warning(message, **{**self.context, **kwargs})
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message with context."""
        self.logger.error(message, **{**self.context, **kwargs})
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message with context."""
        self.logger.critical(message, **{**self.context, **kwargs})


def get_contextual_logger(name: str, **context) -> ContextualLogger:
    """Get a contextual logger with initial context."""
    return ContextualLogger(name, context)


class AuditLogger:
    """Audit logger for security and compliance logging."""
    
    def __init__(self):
        """Initialize audit logger."""
        self.logger = structlog.get_logger("audit")
    
    def log_data_access(self, table: str, operation: str, user: str, **kwargs) -> None:
        """Log data access events."""
        self.logger.info(
            "Data access event",
            event_type="data_access",
            table=table,
            operation=operation,
            user=user,
            **kwargs
        )
    
    def log_configuration_change(self, config_key: str, old_value: Any, new_value: Any, user: str) -> None:
        """Log configuration changes."""
        self.logger.info(
            "Configuration change",
            event_type="config_change",
            config_key=config_key,
            old_value=old_value,
            new_value=new_value,
            user=user
        )
    
    def log_security_event(self, event_type: str, severity: str, **kwargs) -> None:
        """Log security events."""
        self.logger.warning(
            "Security event",
            event_type=event_type,
            severity=severity,
            **kwargs
        )
    
    def log_system_event(self, event_type: str, **kwargs) -> None:
        """Log system events."""
        self.logger.info(
            "System event",
            event_type=event_type,
            **kwargs
        )


def get_audit_logger() -> AuditLogger:
    """Get audit logger instance."""
    return AuditLogger()
