# Troubleshooting Guide

This guide helps diagnose and resolve common issues with the PostgreSQL to StarRocks sync application.

## Quick Diagnostics

### Health Check Commands

```bash
# Check application health
curl -f http://localhost:8080/health

# Check detailed health
curl http://localhost:8080/health/detailed

# Check metrics
curl http://localhost:9090/metrics

# Check logs
docker-compose logs -f sync-app
```

### Service Status

```bash
# Docker Compose
docker-compose ps
docker-compose logs

# Kubernetes
kubectl get pods -n postgres-starrocks-sync
kubectl logs -n postgres-starrocks-sync -l app=sync-app
```

## Common Issues

### 1. Application Startup Issues

#### Symptoms
- Application fails to start
- Health checks failing
- Error messages in logs

#### Diagnosis
```bash
# Check application logs
docker-compose logs sync-app

# Check configuration
python -c "from config_manager import ProductionConfigManager; config = ProductionConfigManager()"

# Verify environment variables
env | grep -E "(POSTGRES|STARROCKS|FLINK)"
```

#### Solutions

**Configuration Issues:**
```bash
# Validate configuration file
python -c "
import yaml
with open('production/config/production_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    print('Configuration is valid')
"

# Check required fields
grep -E "(host|port|database|username|password)" production/config/production_config.yaml
```

**Missing Dependencies:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

**Port Conflicts:**
```bash
# Check port usage
netstat -tulpn | grep -E ":(5432|8030|8080|9090|3000)"

# Kill processes using ports
sudo lsof -ti:5432 | xargs kill -9
```

### 2. Database Connection Issues

#### Symptoms
- "Connection refused" errors
- "Authentication failed" errors
- Timeout errors

#### Diagnosis
```bash
# Test PostgreSQL connection
docker exec demo_postgres pg_isready -U demo_user
psql -h localhost -p 5432 -U demo_user -d demo_db -c "SELECT 1"

# Test StarRocks connection
curl http://localhost:8030/api/bootstrap
```

#### Solutions

**PostgreSQL Issues:**
```bash
# Check PostgreSQL status
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check PostgreSQL configuration
docker exec demo_postgres cat /var/lib/postgresql/data/postgresql.conf | grep -E "(port|listen_addresses)"
```

**StarRocks Issues:**
```bash
# Check StarRocks logs
docker-compose logs starrocks-fe
docker-compose logs starrocks-be

# Restart StarRocks
docker-compose restart starrocks-fe starrocks-be

# Check StarRocks configuration
curl http://localhost:8030/api/bootstrap
```

**Network Issues:**
```bash
# Test network connectivity
ping postgres
ping starrocks-fe

# Check DNS resolution
nslookup postgres
nslookup starrocks-fe
```

### 3. Flink Job Issues

#### Symptoms
- Jobs not starting
- Jobs failing repeatedly
- Checkpoint failures

#### Diagnosis
```bash
# Check Flink UI
open http://localhost:8081

# Check Flink logs
docker-compose logs flink-jobmanager
docker-compose logs flink-taskmanager

# Check job status
curl http://localhost:8081/jobs
```

#### Solutions

**Job Configuration Issues:**
```yaml
# Check Flink configuration in docker-compose.yml
flink:
  jobmanager:
    environment:
      - FLINK_PROPERTIES=...
```

**Resource Issues:**
```bash
# Check system resources
docker stats

# Increase memory limits
# Edit docker-compose.yml
environment:
  - taskmanager.memory.process.size=4096m
```

**Checkpoint Issues:**
```bash
# Check checkpoint configuration
curl http://localhost:8081/jobs/{job-id}/checkpoints

# Restart with clean state
docker-compose down -v
docker-compose up -d
```

### 4. Data Sync Issues

#### Symptoms
- No data being synced
- Partial data sync
- Data inconsistencies

#### Diagnosis
```bash
# Check sync job status
curl http://localhost:8080/health/detailed

# Check metrics
curl http://localhost:9090/metrics | grep sync_records

# Check source data
docker exec demo_postgres psql -U demo_user -d demo_db -c "SELECT COUNT(*) FROM users;"

# Check target data
# (Connect to StarRocks and check target tables)
```

#### Solutions

**CDC Configuration Issues:**
```yaml
# Check CDC configuration
cdc:
  enabled: true
  startup_mode: "initial"
  poll_interval_ms: 1000
```

**Table Schema Issues:**
```sql
-- Check source table schema
\d users

-- Check if replication is enabled
SELECT * FROM pg_publication;
SELECT * FROM pg_replication_slots;
```

**Data Type Mismatches:**
```yaml
# Ensure column types match between source and target
tables:
  - source_table: "users"
    target_table: "users"
    columns:
      - "id"      # BIGINT
      - "name"    # STRING
      - "email"   # STRING
```

### 5. Performance Issues

#### Symptoms
- Slow processing
- High memory usage
- High CPU usage

#### Diagnosis
```bash
# Check system resources
docker stats
htop

# Check application metrics
curl http://localhost:9090/metrics | grep -E "(latency|throughput|memory)"

# Check Flink metrics
curl http://localhost:8081/jobs/{job-id}/metrics
```

#### Solutions

**Memory Issues:**
```yaml
# Increase Flink memory
flink:
  jobmanager:
    environment:
      - jobmanager.memory.process.size=2048m
      - taskmanager.memory.process.size=4096m
```

**CPU Issues:**
```yaml
# Adjust parallelism
flink:
  parallelism: 4  # Increase based on CPU cores
```

**Batch Size Issues:**
```yaml
# Adjust batch sizes
tables:
  - source_table: "users"
    batch_size: 1000  # Increase for better throughput
```

### 6. Monitoring Issues

#### Symptoms
- Metrics not appearing
- Dashboards not loading
- Alerts not firing

#### Diagnosis
```bash
# Check Prometheus status
curl http://localhost:9090/-/healthy

# Check Grafana status
curl http://localhost:3000/api/health

# Check metrics endpoint
curl http://localhost:9090/metrics
```

#### Solutions

**Prometheus Issues:**
```bash
# Check Prometheus configuration
docker-compose logs prometheus

# Restart Prometheus
docker-compose restart prometheus

# Check targets
curl http://localhost:9090/api/v1/targets
```

**Grafana Issues:**
```bash
# Check Grafana logs
docker-compose logs grafana

# Restart Grafana
docker-compose restart grafana

# Check data sources
curl http://localhost:3000/api/datasources
```

## Error Codes and Messages

### Common Error Messages

#### Database Errors
```
ERROR: connection to server at "postgres" (172.18.0.2), port 5432 failed: Connection refused
```
**Solution:** Check PostgreSQL service status and network connectivity

```
ERROR: authentication failed for user "postgres"
```
**Solution:** Verify username and password in configuration

#### Flink Errors
```
Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
```
**Solution:** Increase Flink memory settings

```
Could not find any factory for identifier 'postgres-cdc'
```
**Solution:** Ensure Flink CDC connector is properly configured

#### Application Errors
```
Configuration validation failed: Missing required field 'postgres.host'
```
**Solution:** Check configuration file for required fields

```
Error starting sync job: Table 'users' not found
```
**Solution:** Verify table exists in source database

### Error Code Reference

| Code | Description | Solution |
|------|-------------|----------|
| DB001 | Database connection failed | Check database service and network |
| DB002 | Authentication failed | Verify credentials |
| DB003 | Table not found | Check table exists and permissions |
| FL001 | Flink job failed | Check Flink logs and configuration |
| FL002 | Checkpoint failed | Check storage and network |
| CF001 | Configuration invalid | Validate configuration file |
| CF002 | Missing required field | Check configuration completeness |
| SY001 | Sync job error | Check table configuration and data |

## Debugging Tools

### Log Analysis

```bash
# Filter logs by level
docker-compose logs sync-app | grep ERROR

# Follow logs in real-time
docker-compose logs -f sync-app

# Search for specific patterns
docker-compose logs sync-app | grep -E "(error|exception|failed)"
```

### Metrics Analysis

```bash
# Get specific metrics
curl http://localhost:9090/api/v1/query?query=sync_records_processed_total

# Get metric range
curl "http://localhost:9090/api/v1/query_range?query=sync_records_processed_total&start=2024-01-15T10:00:00Z&end=2024-01-15T11:00:00Z&step=1m"
```

### Database Debugging

```sql
-- Check PostgreSQL replication
SELECT * FROM pg_publication;
SELECT * FROM pg_replication_slots;
SELECT * FROM pg_stat_replication;

-- Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables WHERE schemaname = 'public';

-- Check recent changes
SELECT * FROM users ORDER BY updated_at DESC LIMIT 10;
```

### Network Debugging

```bash
# Test connectivity
telnet postgres 5432
telnet starrocks-fe 8030

# Check DNS resolution
nslookup postgres
nslookup starrocks-fe

# Check port usage
netstat -tulpn | grep -E ":(5432|8030|8080|9090)"
```

## Recovery Procedures

### Application Recovery

```bash
# Restart application
docker-compose restart sync-app

# Clean restart
docker-compose down
docker-compose up -d

# Reset with clean state
docker-compose down -v
docker-compose up -d
```

### Data Recovery

```bash
# Restore from backup
docker exec demo_postgres psql -U demo_user -d demo_db < backup.sql

# Reset target database
# (Connect to StarRocks and truncate target tables)

# Restart sync with initial snapshot
# (Set startup_mode to "initial" in configuration)
```

### Configuration Recovery

```bash
# Restore configuration from backup
cp config/production_config.yaml.backup config/production_config.yaml

# Validate configuration
python -c "from config_manager import ProductionConfigManager; config = ProductionConfigManager()"

# Restart application
docker-compose restart sync-app
```

## Prevention

### Regular Maintenance

1. **Monitor System Health**
   - Check logs regularly
   - Monitor metrics and alerts
   - Review performance trends

2. **Backup Configuration**
   - Version control configuration files
   - Regular configuration backups
   - Document configuration changes

3. **Test Procedures**
   - Regular health checks
   - Disaster recovery testing
   - Performance testing

4. **Update Dependencies**
   - Regular security updates
   - Dependency version updates
   - Compatibility testing

### Best Practices

1. **Configuration Management**
   - Use environment variables for secrets
   - Validate configuration on startup
   - Document all configuration options

2. **Error Handling**
   - Implement proper error handling
   - Use structured logging
   - Set up alerting for critical errors

3. **Monitoring**
   - Comprehensive health checks
   - Performance monitoring
   - Alerting for critical issues

4. **Documentation**
   - Keep troubleshooting guides updated
   - Document common issues and solutions
   - Maintain runbooks for operations

## Getting Help

### Log Collection

When reporting issues, collect:

1. **Application Logs**
   ```bash
   docker-compose logs sync-app > sync-app.log
   ```

2. **System Logs**
   ```bash
   docker-compose logs > system.log
   ```

3. **Configuration**
   ```bash
   cp production/config/production_config.yaml config-backup.yaml
   ```

4. **Health Status**
   ```bash
   curl http://localhost:8080/health/detailed > health.json
   ```

### Support Channels

- **Documentation:** Check this troubleshooting guide
- **Logs:** Review application and system logs
- **Metrics:** Check monitoring dashboards
- **Community:** GitHub issues and discussions
