"""
Comprehensive error handling and retry mechanisms for the production sync application.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, List, Callable, Type
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import traceback
import json
from functools import wraps

import structlog
from sentry_sdk import capture_exception, add_breadcrumb, set_tag, set_context

from config_manager import ProductionConfigManager

logger = structlog.get_logger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories."""
    CONNECTION = "connection"
    DATA_VALIDATION = "data_validation"
    PROCESSING = "processing"
    CHECKPOINT = "checkpoint"
    CONFIGURATION = "configuration"
    SYSTEM = "system"
    UNKNOWN = "unknown"


@dataclass
class ErrorContext:
    """Context information for an error."""
    table: Optional[str] = None
    operation: Optional[str] = None
    batch_id: Optional[str] = None
    checkpoint_id: Optional[str] = None
    retry_count: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    additional_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SyncError:
    """Represents a synchronization error."""
    error_type: str
    message: str
    severity: ErrorSeverity
    category: ErrorCategory
    context: ErrorContext
    original_exception: Optional[Exception] = None
    retryable: bool = True
    max_retries: int = 3
    retry_delay: int = 5000  # milliseconds


class RetryableError(Exception):
    """Exception that can be retried."""
    pass


class NonRetryableError(Exception):
    """Exception that should not be retried."""
    pass


class ErrorHandler:
    """Comprehensive error handling and retry mechanism."""
    
    def __init__(self, config: ProductionConfigManager):
        """Initialize error handler."""
        self.config = config
        self.error_counts: Dict[str, int] = {}
        self.error_history: List[SyncError] = []
        self.dead_letter_queue: List[SyncError] = []
        self.retry_queues: Dict[str, List[SyncError]] = {}
        
        # Setup Sentry if configured
        self._setup_sentry()
        
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
    
    def _setup_sentry(self) -> None:
        """Setup Sentry for error tracking."""
        try:
            import sentry_sdk
            from sentry_sdk.integrations.logging import LoggingIntegration
            
            # Configure Sentry
            sentry_logging = LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            )
            
            sentry_sdk.init(
                dsn=os.getenv('SENTRY_DSN'),
                integrations=[sentry_logging],
                traces_sample_rate=0.1,
                environment=os.getenv('ENVIRONMENT', 'production')
            )
            
            logger.info("Sentry configured for error tracking")
            
        except Exception as e:
            logger.warning(f"Failed to setup Sentry: {e}")
    
    async def handle_error(
        self, 
        exception: Exception, 
        context: str,
        error_context: Optional[ErrorContext] = None
    ) -> None:
        """Handle an error with comprehensive logging and retry logic."""
        try:
            # Create error context if not provided
            if error_context is None:
                error_context = ErrorContext()
            
            # Classify the error
            sync_error = self._classify_error(exception, error_context)
            
            # Log the error
            await self._log_error(sync_error)
            
            # Send to monitoring systems
            await self._send_to_monitoring(sync_error)
            
            # Handle retry logic
            if sync_error.retryable:
                await self._handle_retry(sync_error)
            else:
                await self._handle_non_retryable_error(sync_error)
            
            # Update error counts
            self._update_error_counts(sync_error)
            
            # Add to error history
            self.error_history.append(sync_error)
            
            # Limit error history size
            if len(self.error_history) > 1000:
                self.error_history = self.error_history[-500:]
                
        except Exception as e:
            logger.error(f"Error in error handler: {e}", exc_info=True)
    
    def _classify_error(self, exception: Exception, context: ErrorContext) -> SyncError:
        """Classify an error and determine its properties."""
        error_type = type(exception).__name__
        message = str(exception)
        
        # Determine severity
        severity = self._determine_severity(exception, context)
        
        # Determine category
        category = self._determine_category(exception, context)
        
        # Determine if retryable
        retryable = self._is_retryable(exception, context)
        
        # Get retry configuration
        max_retries = self.config.error_handling.max_retries
        retry_delay = self.config.error_handling.retry_delay
        
        return SyncError(
            error_type=error_type,
            message=message,
            severity=severity,
            category=category,
            context=context,
            original_exception=exception,
            retryable=retryable,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
    
    def _determine_severity(self, exception: Exception, context: ErrorContext) -> ErrorSeverity:
        """Determine error severity based on exception and context."""
        if isinstance(exception, (ConnectionError, TimeoutError)):
            return ErrorSeverity.HIGH
        elif isinstance(exception, (ValueError, TypeError)):
            return ErrorSeverity.MEDIUM
        elif isinstance(exception, (KeyboardInterrupt, SystemExit)):
            return ErrorSeverity.CRITICAL
        else:
            return ErrorSeverity.MEDIUM
    
    def _determine_category(self, exception: Exception, context: ErrorContext) -> ErrorCategory:
        """Determine error category based on exception type."""
        if isinstance(exception, (ConnectionError, TimeoutError)):
            return ErrorCategory.CONNECTION
        elif isinstance(exception, (ValueError, TypeError)):
            return ErrorCategory.DATA_VALIDATION
        elif isinstance(exception, (MemoryError, OSError)):
            return ErrorCategory.SYSTEM
        else:
            return ErrorCategory.UNKNOWN
    
    def _is_retryable(self, exception: Exception, context: ErrorContext) -> bool:
        """Determine if an error is retryable."""
        if isinstance(exception, (KeyboardInterrupt, SystemExit)):
            return False
        elif isinstance(exception, (ValueError, TypeError)):
            return False
        elif isinstance(exception, (ConnectionError, TimeoutError)):
            return True
        else:
            return True
    
    async def _log_error(self, sync_error: SyncError) -> None:
        """Log error with structured logging."""
        log_data = {
            "error_type": sync_error.error_type,
            "message": sync_error.message,
            "severity": sync_error.severity.value,
            "category": sync_error.category.value,
            "table": sync_error.context.table,
            "operation": sync_error.context.operation,
            "retry_count": sync_error.context.retry_count,
            "retryable": sync_error.retryable,
            "timestamp": sync_error.context.timestamp.isoformat()
        }
        
        if sync_error.original_exception:
            log_data["traceback"] = traceback.format_exc()
        
        if sync_error.severity == ErrorSeverity.CRITICAL:
            logger.critical("Critical error occurred", **log_data)
        elif sync_error.severity == ErrorSeverity.HIGH:
            logger.error("High severity error occurred", **log_data)
        elif sync_error.severity == ErrorSeverity.MEDIUM:
            logger.warning("Medium severity error occurred", **log_data)
        else:
            logger.info("Low severity error occurred", **log_data)
    
    async def _send_to_monitoring(self, sync_error: SyncError) -> None:
        """Send error to monitoring systems."""
        try:
            # Send to Sentry
            if sync_error.original_exception:
                capture_exception(sync_error.original_exception)
            
            # Add breadcrumb for context
            add_breadcrumb(
                message=f"Error in {sync_error.context.operation}",
                category="error",
                level="error",
                data={
                    "table": sync_error.context.table,
                    "error_type": sync_error.error_type,
                    "severity": sync_error.severity.value
                }
            )
            
            # Set tags and context
            set_tag("error_category", sync_error.category.value)
            set_tag("error_severity", sync_error.severity.value)
            set_context("error_details", {
                "table": sync_error.context.table,
                "operation": sync_error.context.operation,
                "retry_count": sync_error.context.retry_count
            })
            
        except Exception as e:
            logger.warning(f"Failed to send error to monitoring: {e}")
    
    async def _handle_retry(self, sync_error: SyncError) -> None:
        """Handle retryable errors."""
        if sync_error.context.retry_count >= sync_error.max_retries:
            logger.error(
                f"Error exceeded max retries for {sync_error.context.table}: "
                f"{sync_error.error_type}"
            )
            await self._send_to_dead_letter_queue(sync_error)
            return
        
        # Calculate retry delay with exponential backoff
        delay = self._calculate_retry_delay(sync_error)
        
        logger.info(
            f"Retrying error for {sync_error.context.table} in {delay}ms "
            f"(attempt {sync_error.context.retry_count + 1}/{sync_error.max_retries})"
        )
        
        # Schedule retry
        asyncio.create_task(self._schedule_retry(sync_error, delay))
    
    async def _handle_non_retryable_error(self, sync_error: SyncError) -> None:
        """Handle non-retryable errors."""
        logger.error(
            f"Non-retryable error for {sync_error.context.table}: "
            f"{sync_error.error_type} - {sync_error.message}"
        )
        
        await self._send_to_dead_letter_queue(sync_error)
    
    def _calculate_retry_delay(self, sync_error: SyncError) -> int:
        """Calculate retry delay with exponential backoff."""
        base_delay = sync_error.retry_delay
        
        if self.config.error_handling.exponential_backoff:
            delay = base_delay * (2 ** sync_error.context.retry_count)
            max_delay = self.config.error_handling.max_retry_delay
            return min(delay, max_delay)
        else:
            return base_delay
    
    async def _schedule_retry(self, sync_error: SyncError, delay: int) -> None:
        """Schedule a retry after delay."""
        await asyncio.sleep(delay / 1000.0)  # Convert to seconds
        
        # Increment retry count
        sync_error.context.retry_count += 1
        
        # Retry the operation
        try:
            # This would call the actual retry logic
            # Implementation depends on the specific operation
            await self._execute_retry(sync_error)
            
        except Exception as e:
            # Handle retry failure
            await self.handle_error(e, "retry_failed", sync_error.context)
    
    async def _execute_retry(self, sync_error: SyncError) -> None:
        """Execute the retry logic."""
        # This is a placeholder - actual implementation would depend on
        # the specific operation being retried
        logger.info(f"Executing retry for {sync_error.context.table}")
    
    async def _send_to_dead_letter_queue(self, sync_error: SyncError) -> None:
        """Send error to dead letter queue."""
        if self.config.error_handling.dead_letter_queue:
            self.dead_letter_queue.append(sync_error)
            logger.info(f"Error sent to dead letter queue: {sync_error.error_type}")
    
    def _update_error_counts(self, sync_error: SyncError) -> None:
        """Update error counts for monitoring."""
        key = f"{sync_error.context.table}_{sync_error.error_type}"
        self.error_counts[key] = self.error_counts.get(key, 0) + 1
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of current errors."""
        return {
            "total_errors": len(self.error_history),
            "error_counts": self.error_counts,
            "dead_letter_queue_size": len(self.dead_letter_queue),
            "recent_errors": [
                {
                    "error_type": error.error_type,
                    "table": error.context.table,
                    "severity": error.severity.value,
                    "timestamp": error.context.timestamp.isoformat()
                }
                for error in self.error_history[-10:]  # Last 10 errors
            ]
        }
    
    def retry_with_backoff(
        self,
        max_retries: int = 3,
        base_delay: int = 1000,
        max_delay: int = 30000,
        exponential_base: float = 2.0
    ):
        """Decorator for retrying functions with exponential backoff."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        
                        if attempt == max_retries:
                            logger.error(f"Function {func.__name__} failed after {max_retries} retries")
                            raise
                        
                        # Calculate delay
                        delay = min(base_delay * (exponential_base ** attempt), max_delay)
                        
                        logger.warning(
                            f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}), "
                            f"retrying in {delay}ms: {e}"
                        )
                        
                        await asyncio.sleep(delay / 1000.0)
                
                raise last_exception
            
            return wrapper
        return decorator
