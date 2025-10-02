# Demo Setup Guide

This guide will help you set up and run the PostgreSQL to StarRocks sync demo with 2x2 tables.

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB of available RAM
- Ports 5432, 8030, 8081, 8080, 9090, 3000 available

## Quick Start

1. **Clone and navigate to the demo directory:**
   ```bash
   cd demo
   ```

2. **Start the demo environment:**
   ```bash
   docker-compose up -d
   ```

3. **Wait for services to start (about 2-3 minutes):**
   ```bash
   docker-compose logs -f
   ```

4. **Verify the setup:**
   - PostgreSQL: `docker exec demo_postgres pg_isready -U demo_user`
   - StarRocks: Check http://localhost:8030
   - Flink UI: Check http://localhost:8081
   - Sync App: Check http://localhost:8080/health

## Demo Tables

The demo includes 2 tables that will be synchronized:

### Users Table
- **Source:** PostgreSQL `users` table
- **Target:** StarRocks `users` table
- **Columns:** id, username, email, created_at, updated_at

### Orders Table
- **Source:** PostgreSQL `orders` table
- **Target:** StarRocks `orders` table
- **Columns:** id, user_id, product_name, quantity, price, status, created_at, updated_at

## Testing the Demo

1. **Insert test data in PostgreSQL:**
   ```sql
   -- Connect to PostgreSQL
   docker exec -it demo_postgres psql -U demo_user -d demo_db
   
   -- Insert test data
   INSERT INTO users (username, email) VALUES ('test_user', 'test@example.com');
   INSERT INTO orders (user_id, product_name, quantity, price) VALUES (1, 'Test Product', 1, 99.99);
   ```

2. **Verify data in StarRocks:**
   ```sql
   -- Connect to StarRocks (if you have a client)
   -- Or check the Flink UI for processing metrics
   ```

3. **Monitor the sync process:**
   - Check Flink UI: http://localhost:8081
   - Check application logs: `docker-compose logs -f sync-app`

## Configuration

The demo uses the configuration file `demo/config/demo_config.yaml`. Key settings:

- **PostgreSQL:** localhost:5432, database: demo_db
- **StarRocks:** localhost:8030, database: demo_db
- **Flink:** localhost:8081, parallelism: 1
- **CDC:** Initial snapshot mode, 1-second poll interval

## Monitoring

### Health Checks
- **Application Health:** http://localhost:8080/health
- **Readiness:** http://localhost:8080/health/ready
- **Liveness:** http://localhost:8080/health/live

### Metrics
- **Application Metrics:** http://localhost:9090/metrics
- **Flink Metrics:** Available in Flink UI

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f sync-app
docker-compose logs -f postgres
docker-compose logs -f starrocks-fe
```

## Troubleshooting

### Common Issues

1. **Services not starting:**
   ```bash
   # Check service status
   docker-compose ps
   
   # Check logs
   docker-compose logs
   ```

2. **Port conflicts:**
   ```bash
   # Check if ports are in use
   netstat -tulpn | grep :5432
   netstat -tulpn | grep :8030
   ```

3. **Database connection issues:**
   ```bash
   # Test PostgreSQL connection
   docker exec demo_postgres pg_isready -U demo_user
   
   # Check StarRocks status
   curl http://localhost:8030/api/bootstrap
   ```

4. **Flink job not starting:**
   - Check Flink UI: http://localhost:8081
   - Look for error messages in the job overview
   - Check application logs for CDC connector issues

### Reset Demo

To reset the demo environment:

```bash
# Stop and remove all containers
docker-compose down -v

# Remove images (optional)
docker-compose down --rmi all

# Start fresh
docker-compose up -d
```

## Next Steps

After running the demo successfully:

1. **Explore the Production Setup:** Check out the `production/` directory for a full-featured implementation
2. **Customize Configuration:** Modify `demo_config.yaml` to test different scenarios
3. **Add More Tables:** Extend the demo with additional tables
4. **Monitor Performance:** Use the built-in metrics to understand performance characteristics

## Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify all services are healthy: `docker-compose ps`
3. Check the troubleshooting section above
4. Review the main README.md for additional information
