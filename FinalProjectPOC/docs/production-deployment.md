# Production Deployment Guide

This guide covers deploying the PostgreSQL to StarRocks sync application in a production environment.

## Prerequisites

### System Requirements
- **CPU:** 8+ cores recommended
- **Memory:** 16GB+ RAM recommended
- **Storage:** 100GB+ available disk space
- **Network:** Stable network connectivity between components

### Software Requirements
- **Docker:** 20.10+ and Docker Compose 2.0+
- **Kubernetes:** 1.20+ (for K8s deployment)
- **kubectl:** Latest version
- **PostgreSQL:** 12+ with logical replication enabled
- **StarRocks:** 2.0+ with appropriate cluster setup

## Deployment Options

### Option 1: Docker Compose (Recommended for small to medium deployments)

#### 1. Prepare Environment

```bash
# Clone the repository
git clone <repository-url>
cd postgres-starrocks-sync

# Navigate to production deployment
cd production/deployment
```

#### 2. Configure Environment

```bash
# Copy and edit environment file
cp .env.example .env

# Edit configuration
nano .env
```

Key environment variables:
```bash
# Database Configuration
POSTGRES_DB=production_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

STARROCKS_DB=production_db
STARROCKS_USER=root
STARROCKS_PASSWORD=your_secure_password

# Monitoring
GRAFANA_PASSWORD=your_grafana_password

# Security
SENTRY_DSN=your_sentry_dsn
ALERT_WEBHOOK_URL=your_webhook_url
SLACK_WEBHOOK=your_slack_webhook
```

#### 3. Deploy

```bash
# Make deployment script executable
chmod +x scripts/deploy.sh

# Deploy with Docker Compose
./scripts/deploy.sh docker
```

#### 4. Verify Deployment

```bash
# Check service status
docker-compose ps

# Check health endpoints
curl http://localhost:8080/health
curl http://localhost:9090/-/healthy
curl http://localhost:3000/api/health

# View logs
docker-compose logs -f sync-app
```

### Option 2: Kubernetes (Recommended for large deployments)

#### 1. Prepare Kubernetes Cluster

```bash
# Ensure kubectl is configured
kubectl cluster-info

# Verify cluster resources
kubectl top nodes
```

#### 2. Configure Secrets

```bash
# Create secrets
kubectl create secret generic sync-secrets \
  --from-literal=postgres-password=your_secure_password \
  --from-literal=starrocks-password=your_secure_password \
  --from-literal=grafana-password=your_grafana_password \
  --from-literal=sentry-dsn=your_sentry_dsn \
  --from-literal=alert-webhook-url=your_webhook_url \
  --from-literal=slack-webhook=your_slack_webhook \
  -n postgres-starrocks-sync
```

#### 3. Deploy

```bash
# Deploy to Kubernetes
./scripts/deploy.sh k8s
```

#### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n postgres-starrocks-sync

# Check services
kubectl get services -n postgres-starrocks-sync

# Port forward for testing
kubectl port-forward -n postgres-starrocks-sync service/sync-app-service 8080:8080
kubectl port-forward -n postgres-starrocks-sync service/prometheus-service 9090:9090
kubectl port-forward -n postgres-starrocks-sync service/grafana-service 3000:3000
```

## Configuration

### Production Configuration

The production configuration is located in `production/config/production_config.yaml`. Key sections:

#### Database Configuration
```yaml
postgres:
  host: "your-postgres-host"
  port: 5432
  database: "production_db"
  username: "postgres"
  password: "secure_password"
  connection_pool_size: 20
  connection_timeout: 30

starrocks:
  host: "your-starrocks-host"
  port: 8030
  database: "production_db"
  username: "root"
  password: "secure_password"
  buffer_flush_max_rows: 5000
  buffer_flush_interval: "5s"
```

#### Flink Configuration
```yaml
flink:
  parallelism: 8
  checkpoint_interval: 30000
  checkpoint_timeout: 600000
  checkpointing_mode: "EXACTLY_ONCE"
  restart_strategy: "exponential-delay"
  restart_attempts: 5
```

#### Monitoring Configuration
```yaml
monitoring:
  enabled: true
  metrics_port: 9090
  health_check_port: 8080
  alert_thresholds:
    error_rate: 0.01
    latency_p99: 500.0
    throughput_min: 1000.0
```

### Table Configuration

Configure tables to sync in the `tables` section:

```yaml
tables:
  - source_table: "users"
    target_table: "users"
    primary_key: "id"
    columns:
      - "id"
      - "username"
      - "email"
      - "created_at"
      - "updated_at"
    sync_mode: "cdc"
    batch_size: 2000
    enabled: true
```

## Monitoring and Observability

### Health Checks

- **Application Health:** `GET /health`
- **Readiness:** `GET /health/ready`
- **Liveness:** `GET /health/live`
- **Detailed Health:** `GET /health/detailed`

### Metrics

- **Prometheus Metrics:** `http://localhost:9090/metrics`
- **Application Metrics:** Available at `/metrics` endpoint
- **Custom Dashboards:** Available in Grafana

### Logging

- **Structured Logging:** JSON format with context
- **Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Rotation:** Automatic with configurable retention
- **Centralized Logging:** Compatible with ELK stack

### Alerting

Configure alerts in `production_config.yaml`:

```yaml
alerting:
  enabled: true
  webhook_url: "https://your-webhook-url"
  rules:
    - name: "high_error_rate"
      condition: "error_rate > 0.05"
      severity: "warning"
      cooldown: 300
```

## Security

### Network Security
- Use TLS/SSL for all connections
- Configure firewall rules
- Use VPN or private networks for database access

### Authentication
- Use strong passwords for all services
- Enable authentication for monitoring tools
- Configure RBAC for Kubernetes deployments

### Data Protection
- Enable encryption at rest
- Use encrypted connections
- Implement audit logging
- Regular security updates

## Performance Tuning

### Flink Tuning
- Adjust parallelism based on CPU cores
- Configure checkpoint intervals
- Tune memory settings
- Optimize network settings

### Database Tuning
- Configure connection pools
- Optimize query performance
- Set appropriate timeouts
- Monitor resource usage

### Application Tuning
- Configure batch sizes
- Tune retry mechanisms
- Optimize error handling
- Monitor memory usage

## Backup and Recovery

### Data Backup
- Regular PostgreSQL backups
- StarRocks data backups
- Configuration backups
- Log retention policies

### Disaster Recovery
- Multi-region deployment
- Automated failover
- Data replication
- Recovery procedures

## Maintenance

### Regular Tasks
- Monitor system health
- Review logs and metrics
- Update dependencies
- Security patches

### Scaling
- Horizontal scaling with Kubernetes
- Vertical scaling for resource constraints
- Load balancing
- Auto-scaling policies

## Troubleshooting

### Common Issues

1. **High Memory Usage**
   - Check Flink memory settings
   - Monitor garbage collection
   - Adjust batch sizes

2. **Connection Issues**
   - Verify network connectivity
   - Check firewall rules
   - Validate credentials

3. **Performance Issues**
   - Monitor CPU and memory usage
   - Check disk I/O
   - Review Flink metrics

4. **Data Sync Issues**
   - Check CDC configuration
   - Verify table schemas
   - Monitor error logs

### Debug Commands

```bash
# Check application status
curl http://localhost:8080/health/detailed

# View metrics
curl http://localhost:9090/metrics

# Check logs
docker-compose logs -f sync-app

# Monitor resources
docker stats
```

## Support and Maintenance

### Monitoring
- Set up alerting for critical issues
- Regular health checks
- Performance monitoring
- Capacity planning

### Updates
- Regular dependency updates
- Security patches
- Feature updates
- Configuration changes

### Documentation
- Keep documentation updated
- Document configuration changes
- Maintain runbooks
- Share knowledge with team

## Next Steps

After successful deployment:

1. **Configure Monitoring:** Set up dashboards and alerts
2. **Test Failover:** Verify disaster recovery procedures
3. **Performance Testing:** Load test the system
4. **Security Audit:** Review security configurations
5. **Documentation:** Create operational runbooks
