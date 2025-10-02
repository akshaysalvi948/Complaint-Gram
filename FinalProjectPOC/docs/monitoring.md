# Monitoring Guide

This guide covers monitoring, observability, and alerting for the PostgreSQL to StarRocks sync application.

## Overview

The application provides comprehensive monitoring capabilities including:

- **Health Checks:** Application and component health monitoring
- **Metrics:** Performance and operational metrics
- **Logging:** Structured logging with context
- **Alerting:** Real-time alerts for critical issues
- **Dashboards:** Visual monitoring interfaces

## Health Monitoring

### Health Endpoints

The application exposes several health check endpoints:

#### Application Health
- **Endpoint:** `GET /health`
- **Purpose:** Overall application health status
- **Response:** JSON with status and component health

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "checks": {
    "postgres_connection": {
      "status": "healthy",
      "message": "PostgreSQL connection is healthy",
      "response_time_ms": 15.2
    },
    "starrocks_connection": {
      "status": "healthy", 
      "message": "StarRocks connection is healthy",
      "response_time_ms": 23.1
    }
  }
}
```

#### Readiness Probe
- **Endpoint:** `GET /health/ready`
- **Purpose:** Kubernetes readiness probe
- **Response:** 200 if ready, 503 if not ready

#### Liveness Probe
- **Endpoint:** `GET /health/live`
- **Purpose:** Kubernetes liveness probe
- **Response:** 200 if alive, 503 if crashed

#### Detailed Health
- **Endpoint:** `GET /health/detailed`
- **Purpose:** Comprehensive health information
- **Response:** Detailed status with metrics

### Health Check Components

The application monitors:

1. **Database Connections**
   - PostgreSQL connectivity
   - StarRocks connectivity
   - Connection pool status

2. **Flink Environment**
   - JobManager availability
   - TaskManager status
   - Job execution status

3. **Sync Jobs**
   - Individual job health
   - Error rates
   - Processing status

4. **System Resources**
   - CPU usage
   - Memory usage
   - Disk space

## Metrics

### Prometheus Metrics

The application exposes metrics in Prometheus format at `/metrics`:

#### Application Metrics
```
# Sync records processed
sync_records_processed_total{table="users", operation="insert"} 1500
sync_records_processed_total{table="orders", operation="update"} 750

# Sync records failed
sync_records_failed_total{table="users", error_type="connection"} 5
sync_records_failed_total{table="orders", error_type="validation"} 2

# Processing latency
sync_processing_latency_seconds_bucket{table="users", operation="insert", le="0.001"} 100
sync_processing_latency_seconds_bucket{table="users", operation="insert", le="0.005"} 500
sync_processing_latency_seconds_bucket{table="users", operation="insert", le="0.01"} 800

# Batch size distribution
sync_batch_size_bucket{table="users", le="1"} 10
sync_batch_size_bucket{table="users", le="5"} 50
sync_batch_size_bucket{table="users", le="10"} 100

# Checkpoint metrics
sync_checkpoints_completed_total{table="users"} 150
sync_checkpoints_failed_total{table="orders"} 3

# Job status
sync_active_jobs 4
sync_error_jobs 0

# Throughput
sync_throughput_records_per_second{table="users"} 250.5
sync_throughput_records_per_second{table="orders"} 180.2

# Lag
sync_lag_seconds{table="users"} 5.2
sync_lag_seconds{table="orders"} 12.8
```

#### System Metrics
```
# CPU usage
node_cpu_seconds_total{mode="idle"} 1500.5
node_cpu_seconds_total{mode="user"} 200.3

# Memory usage
node_memory_MemTotal_bytes 8589934592
node_memory_MemAvailable_bytes 4294967296

# Disk usage
node_filesystem_size_bytes{device="/dev/sda1"} 107374182400
node_filesystem_avail_bytes{device="/dev/sda1"} 53687091200
```

### Custom Metrics

The application tracks custom business metrics:

- **Record Processing Rate:** Records processed per second
- **Error Rate:** Percentage of failed records
- **Latency Percentiles:** P50, P95, P99 processing latency
- **Throughput:** Data volume processed per unit time
- **Lag:** Time difference between source and target
- **Checkpoint Duration:** Time to complete checkpoints
- **Memory Usage:** Application memory consumption
- **Connection Pool Usage:** Database connection utilization

## Logging

### Structured Logging

The application uses structured logging with JSON format:

```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "INFO",
  "logger": "sync_app",
  "message": "Record processed successfully",
  "table": "users",
  "operation": "insert",
  "record_id": "12345",
  "processing_time_ms": 15.2,
  "batch_size": 100
}
```

### Log Levels

- **DEBUG:** Detailed debugging information
- **INFO:** General information about operations
- **WARNING:** Warning messages for potential issues
- **ERROR:** Error messages for failed operations
- **CRITICAL:** Critical errors requiring immediate attention

### Log Context

Logs include contextual information:

- **Table Name:** Which table is being processed
- **Operation Type:** Insert, update, delete
- **Record ID:** Unique identifier for the record
- **Processing Time:** Time taken to process
- **Batch Information:** Batch size and timing
- **Error Details:** Error type and message
- **User Context:** User or system performing operation

### Log Rotation

- **File Size:** Configurable maximum file size
- **Backup Count:** Number of backup files to keep
- **Compression:** Automatic compression of old logs
- **Retention:** Configurable retention period

## Alerting

### Alert Rules

The application includes predefined alert rules:

#### Critical Alerts
- **High Error Rate:** Error rate > 10%
- **No Data Processing:** No records processed in 10 minutes
- **Job Failures:** Sync jobs in error state
- **Database Down:** Database connection failures
- **High Memory Usage:** Memory usage > 90%
- **High CPU Usage:** CPU usage > 90%

#### Warning Alerts
- **Elevated Error Rate:** Error rate > 5%
- **High Latency:** P99 latency > 1 second
- **Low Throughput:** Throughput < 100 records/second
- **Disk Space Low:** Disk usage > 90%
- **Checkpoint Failures:** Frequent checkpoint failures

### Alert Configuration

Configure alerts in `production_config.yaml`:

```yaml
alerting:
  enabled: true
  webhook_url: "https://your-webhook-url"
  slack_webhook: "https://hooks.slack.com/your-webhook"
  pagerduty_integration_key: "your-pagerduty-key"
  
  rules:
    - name: "high_error_rate"
      condition: "error_rate > 0.05"
      severity: "warning"
      cooldown: 300
      
    - name: "critical_error_rate"
      condition: "error_rate > 0.1"
      severity: "critical"
      cooldown: 60
```

### Alert Channels

Supported alert channels:

- **Webhooks:** HTTP POST to custom endpoints
- **Slack:** Direct messages to Slack channels
- **PagerDuty:** Integration with PagerDuty
- **Email:** SMTP email notifications
- **SMS:** SMS notifications via webhooks

## Dashboards

### Grafana Dashboards

The application includes pre-built Grafana dashboards:

#### Application Overview
- System health status
- Processing rates and volumes
- Error rates and types
- Resource utilization

#### Database Monitoring
- Connection pool status
- Query performance
- Replication lag
- Storage usage

#### Flink Monitoring
- Job status and metrics
- Checkpoint information
- Task manager status
- Backpressure indicators

#### Business Metrics
- Records processed by table
- Data freshness
- Processing latency
- Throughput trends

### Dashboard Configuration

Dashboards are automatically provisioned in Grafana:

1. **Data Sources:** Prometheus configured automatically
2. **Dashboards:** Pre-built dashboards imported
3. **Alerts:** Alert rules configured
4. **Variables:** Dashboard variables set up

## Monitoring Tools

### Prometheus

- **Metrics Collection:** Scrapes metrics from all components
- **Alerting:** Evaluates alert rules
- **Storage:** Time-series data storage
- **Querying:** PromQL for metric queries

### Grafana

- **Visualization:** Charts and graphs
- **Dashboards:** Customizable dashboards
- **Alerting:** Visual alert management
- **Annotations:** Event annotations

### Flink UI

- **Job Monitoring:** Real-time job status
- **Metrics:** Flink-specific metrics
- **Checkpoints:** Checkpoint information
- **Backpressure:** Performance indicators

## Best Practices

### Monitoring Strategy

1. **Layered Monitoring**
   - Infrastructure level
   - Application level
   - Business level

2. **Proactive Monitoring**
   - Set up alerts before issues occur
   - Monitor trends and patterns
   - Regular capacity planning

3. **Comprehensive Coverage**
   - All components monitored
   - All critical paths covered
   - All failure modes addressed

### Alert Management

1. **Alert Fatigue Prevention**
   - Appropriate thresholds
   - Cooldown periods
   - Alert grouping

2. **Escalation Procedures**
   - Clear escalation paths
   - On-call rotations
   - Escalation timeouts

3. **Alert Quality**
   - Meaningful alert messages
   - Actionable information
   - Context and troubleshooting

### Performance Monitoring

1. **Key Metrics**
   - Throughput and latency
   - Error rates
   - Resource utilization

2. **Trend Analysis**
   - Historical data analysis
   - Capacity planning
   - Performance optimization

3. **Baseline Establishment**
   - Normal operating ranges
   - Performance baselines
   - Anomaly detection

## Troubleshooting

### Common Monitoring Issues

1. **Missing Metrics**
   - Check metric collection configuration
   - Verify Prometheus scraping
   - Review application logs

2. **False Alerts**
   - Adjust alert thresholds
   - Review alert conditions
   - Check data quality

3. **Dashboard Issues**
   - Verify data source connections
   - Check query syntax
   - Review dashboard configuration

### Debug Commands

```bash
# Check health status
curl http://localhost:8080/health/detailed

# View metrics
curl http://localhost:9090/metrics

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# View application logs
docker-compose logs -f sync-app

# Check Grafana status
curl http://localhost:3000/api/health
```

### Monitoring Checklist

- [ ] All health checks passing
- [ ] Metrics being collected
- [ ] Alerts configured and tested
- [ ] Dashboards displaying correctly
- [ ] Log aggregation working
- [ ] Alert notifications functioning
- [ ] Performance baselines established
- [ ] Monitoring documentation updated
