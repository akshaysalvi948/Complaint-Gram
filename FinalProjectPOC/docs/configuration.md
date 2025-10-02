# Configuration Reference

This document provides a comprehensive reference for all configuration options available in the PostgreSQL to StarRocks sync application.

## Configuration Files

### Demo Configuration
- **File:** `demo/config/demo_config.yaml`
- **Purpose:** Simple configuration for demo/testing
- **Scope:** 2x2 table synchronization

### Production Configuration
- **File:** `production/config/production_config.yaml`
- **Purpose:** Full-featured production configuration
- **Scope:** Complete production deployment

## Configuration Sections

### Database Configuration

#### PostgreSQL Configuration
```yaml
postgres:
  host: "localhost"                    # PostgreSQL hostname
  port: 5432                          # PostgreSQL port
  database: "production_db"            # Database name
  username: "postgres"                 # Username
  password: "password"                 # Password
  schema: "public"                     # Schema name
  connection_pool_size: 20             # Connection pool size
  connection_timeout: 30               # Connection timeout (seconds)
  query_timeout: 300                   # Query timeout (seconds)
```

#### StarRocks Configuration
```yaml
starrocks:
  host: "localhost"                    # StarRocks hostname
  port: 8030                          # StarRocks port
  database: "production_db"            # Database name
  username: "root"                     # Username
  password: "root"                     # Password
  buffer_flush_max_rows: 5000          # Max rows before flush
  buffer_flush_interval: "5s"          # Flush interval
  max_retries: 5                       # Max retry attempts
  retry_delay: 2000                    # Retry delay (ms)
  load_timeout: 600000                 # Load timeout (ms)
```

### Flink Configuration

```yaml
flink:
  jobmanager:
    host: "localhost"                  # JobManager host
    port: 8081                         # JobManager port
  parallelism: 8                       # Default parallelism
  checkpoint_interval: 30000           # Checkpoint interval (ms)
  checkpoint_timeout: 600000           # Checkpoint timeout (ms)
  min_pause_between_checkpoints: 10000 # Min pause between checkpoints (ms)
  max_concurrent_checkpoints: 2        # Max concurrent checkpoints
  checkpointing_mode: "EXACTLY_ONCE"   # Checkpointing mode
  restart_strategy: "exponential-delay" # Restart strategy
  restart_attempts: 5                  # Max restart attempts
  restart_delay: 10000                 # Initial restart delay (ms)
  restart_max_delay: 300000            # Max restart delay (ms)
  restart_backoff_multiplier: 2.0      # Backoff multiplier
```

### Table Configuration

```yaml
tables:
  - source_table: "users"              # Source table name
    target_table: "users"              # Target table name
    primary_key: "id"                  # Primary key column
    columns:                           # Columns to sync
      - "id"
      - "username"
      - "email"
      - "created_at"
      - "updated_at"
    sync_mode: "cdc"                   # Sync mode: cdc, batch, hybrid
    batch_size: 2000                   # Batch size for processing
    sync_interval: 30                  # Sync interval (seconds)
    enabled: true                      # Enable/disable sync
```

### CDC Configuration

```yaml
cdc:
  enabled: true                        # Enable CDC
  startup_mode: "initial"              # Startup mode: initial, latest, timestamp
  snapshot_mode: "initial"             # Snapshot mode
  poll_interval_ms: 500                # Poll interval (ms)
  max_batch_size: 2000                 # Max batch size
  max_wait_time_ms: 3000               # Max wait time (ms)
  snapshot_chunk_size: 16384           # Snapshot chunk size
  snapshot_fetch_size: 2048            # Snapshot fetch size
  heartbeat_interval: 15000            # Heartbeat interval (ms)
  connect_timeout: 30000               # Connection timeout (ms)
  connection_pool_size: 20             # Connection pool size
```

### Monitoring Configuration

```yaml
monitoring:
  enabled: true                        # Enable monitoring
  metrics_port: 9090                   # Metrics port
  health_check_port: 8080              # Health check port
  job_check_interval: 30               # Job check interval (seconds)
  metrics_collection_interval: 10      # Metrics collection interval (seconds)
  alert_thresholds:                    # Alert thresholds
    error_rate: 0.01                   # Error rate threshold
    latency_p99: 500.0                 # P99 latency threshold (ms)
    throughput_min: 1000.0             # Min throughput threshold
    memory_usage: 0.85                 # Memory usage threshold
    cpu_usage: 0.80                    # CPU usage threshold
```

### Error Handling Configuration

```yaml
error_handling:
  max_retries: 5                       # Max retry attempts
  retry_delay: 5000                    # Retry delay (ms)
  exponential_backoff: true            # Use exponential backoff
  max_retry_delay: 300000              # Max retry delay (ms)
  dead_letter_queue: true              # Enable dead letter queue
  alert_on_error: true                 # Alert on errors
  error_notification_webhook: ""       # Error notification webhook
```

### Logging Configuration

```yaml
logging:
  level: "INFO"                        # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Log format
  file: "logs/production_sync.log"     # Log file path
  max_file_size: 52428800              # Max file size (bytes)
  backup_count: 10                     # Number of backup files
  json_format: true                    # Use JSON format
  structured_logging: true             # Enable structured logging
```

### Security Configuration

```yaml
security:
  enable_ssl: false                    # Enable SSL
  ssl_cert_path: ""                    # SSL certificate path
  ssl_key_path: ""                     # SSL key path
  enable_encryption: false             # Enable encryption
  encryption_key: ""                   # Encryption key
  enable_audit_logging: true           # Enable audit logging
```

### Performance Configuration

```yaml
performance:
  max_memory_usage: 0.8                # Max memory usage (80%)
  max_cpu_usage: 0.7                   # Max CPU usage (70%)
  batch_processing_timeout: 300        # Batch processing timeout (seconds)
  connection_pool_exhaustion_threshold: 0.9  # Connection pool threshold
  checkpoint_compression: true         # Enable checkpoint compression
  checkpoint_compression_algorithm: "lz4"  # Compression algorithm
```

### Alerting Configuration

```yaml
alerting:
  enabled: true                        # Enable alerting
  webhook_url: ""                      # Webhook URL
  email_notifications: false           # Email notifications
  email_recipients: []                 # Email recipients
  slack_webhook: ""                    # Slack webhook
  pagerduty_integration_key: ""        # PagerDuty integration key
  
  rules:                               # Alert rules
    - name: "high_error_rate"
      condition: "error_rate > 0.05"
      severity: "warning"
      cooldown: 300                    # Cooldown period (seconds)
```

## Environment Variables

The application supports configuration via environment variables. Environment variables override configuration file values.

### Database Environment Variables
```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=production_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_SCHEMA=public
POSTGRES_POOL_SIZE=20
POSTGRES_TIMEOUT=30
POSTGRES_QUERY_TIMEOUT=300

STARROCKS_HOST=localhost
STARROCKS_PORT=8030
STARROCKS_DB=production_db
STARROCKS_USER=root
STARROCKS_PASSWORD=root
STARROCKS_BUFFER_ROWS=5000
STARROCKS_BUFFER_INTERVAL=5s
STARROCKS_MAX_RETRIES=5
STARROCKS_RETRY_DELAY=2000
STARROCKS_LOAD_TIMEOUT=600000
```

### Flink Environment Variables
```bash
FLINK_JOBMANAGER_HOST=localhost
FLINK_JOBMANAGER_PORT=8081
FLINK_PARALLELISM=8
FLINK_CHECKPOINT_INTERVAL=30000
FLINK_CHECKPOINT_TIMEOUT=600000
FLINK_MIN_PAUSE=10000
FLINK_MAX_CONCURRENT=2
FLINK_CHECKPOINT_MODE=EXACTLY_ONCE
FLINK_RESTART_STRATEGY=exponential-delay
FLINK_RESTART_ATTEMPTS=5
FLINK_RESTART_DELAY=10000
FLINK_RESTART_MAX_DELAY=300000
FLINK_RESTART_BACKOFF=2.0
```

### Monitoring Environment Variables
```bash
MONITORING_ENABLED=true
METRICS_PORT=9090
HEALTH_CHECK_PORT=8080
JOB_CHECK_INTERVAL=30
METRICS_COLLECTION_INTERVAL=10
ALERT_ERROR_RATE=0.01
ALERT_LATENCY_P99=500.0
ALERT_THROUGHPUT_MIN=1000.0
```

### Logging Environment Variables
```bash
LOG_LEVEL=INFO
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE=logs/production_sync.log
LOG_MAX_FILE_SIZE=52428800
LOG_BACKUP_COUNT=10
LOG_JSON_FORMAT=true
LOG_STRUCTURED=true
```

### Security Environment Variables
```bash
SECURITY_ENABLE_SSL=false
SECURITY_SSL_CERT_PATH=""
SECURITY_SSL_KEY_PATH=""
SECURITY_ENABLE_ENCRYPTION=false
SECURITY_ENCRYPTION_KEY=""
SECURITY_AUDIT_LOGGING=true
```

### External Service Environment Variables
```bash
SENTRY_DSN=""
ALERT_WEBHOOK_URL=""
SLACK_WEBHOOK=""
PAGERDUTY_INTEGRATION_KEY=""
```

## Configuration Validation

The application validates configuration on startup and will fail if:

1. **Required fields are missing**
2. **Invalid values are provided**
3. **Conflicting settings are detected**
4. **Database connections cannot be established**

### Validation Rules

- Database hosts must be reachable
- Ports must be valid (1-65535)
- Passwords must be non-empty
- Table configurations must have valid column lists
- Flink parallelism must be positive
- Checkpoint intervals must be reasonable

## Configuration Best Practices

### Security
- Use strong passwords
- Enable SSL in production
- Use environment variables for secrets
- Regular security audits

### Performance
- Tune parallelism based on resources
- Configure appropriate batch sizes
- Set reasonable timeouts
- Monitor resource usage

### Reliability
- Enable checkpointing
- Configure retry mechanisms
- Set up monitoring and alerting
- Regular backups

### Maintainability
- Use structured logging
- Document configuration changes
- Version control configurations
- Regular configuration reviews

## Troubleshooting Configuration

### Common Issues

1. **Database Connection Failures**
   - Check host and port
   - Verify credentials
   - Test network connectivity

2. **Invalid Configuration Values**
   - Check data types
   - Verify ranges
   - Review documentation

3. **Missing Required Fields**
   - Check configuration file
   - Verify environment variables
   - Review validation errors

4. **Performance Issues**
   - Adjust parallelism
   - Tune batch sizes
   - Check resource limits

### Debug Commands

```bash
# Validate configuration
python -c "from config_manager import ProductionConfigManager; config = ProductionConfigManager(); print('Configuration valid')"

# Check environment variables
env | grep -E "(POSTGRES|STARROCKS|FLINK|LOG_)"

# Test database connections
psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT 1"
```

## Configuration Examples

### Minimal Configuration
```yaml
postgres:
  host: "localhost"
  port: 5432
  database: "test_db"
  username: "postgres"
  password: "password"

starrocks:
  host: "localhost"
  port: 8030
  database: "test_db"
  username: "root"
  password: "root"

tables:
  - source_table: "users"
    target_table: "users"
    primary_key: "id"
    columns: ["id", "name", "email"]
```

### Production Configuration
```yaml
postgres:
  host: "prod-postgres.example.com"
  port: 5432
  database: "production_db"
  username: "sync_user"
  password: "${POSTGRES_PASSWORD}"
  connection_pool_size: 50
  connection_timeout: 60

starrocks:
  host: "prod-starrocks.example.com"
  port: 8030
  database: "production_db"
  username: "sync_user"
  password: "${STARROCKS_PASSWORD}"
  buffer_flush_max_rows: 10000
  buffer_flush_interval: "2s"

flink:
  parallelism: 16
  checkpoint_interval: 60000
  checkpointing_mode: "EXACTLY_ONCE"

monitoring:
  enabled: true
  alert_thresholds:
    error_rate: 0.005
    latency_p99: 100.0
    throughput_min: 5000.0
```
