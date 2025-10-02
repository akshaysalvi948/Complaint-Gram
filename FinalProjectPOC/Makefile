# PostgreSQL to StarRocks Sync - Makefile

.PHONY: help install demo production clean test lint format

# Default target
help:
	@echo "PostgreSQL to StarRocks Sync - Available Commands:"
	@echo ""
	@echo "Demo Commands:"
	@echo "  demo-setup     - Set up demo environment"
	@echo "  demo-start     - Start demo services"
	@echo "  demo-stop      - Stop demo services"
	@echo "  demo-logs      - View demo logs"
	@echo "  demo-clean     - Clean demo environment"
	@echo ""
	@echo "Production Commands:"
	@echo "  prod-build     - Build production Docker image"
	@echo "  prod-deploy    - Deploy production (Docker Compose)"
	@echo "  prod-k8s       - Deploy production (Kubernetes)"
	@echo "  prod-stop      - Stop production services"
	@echo "  prod-logs      - View production logs"
	@echo "  prod-clean     - Clean production environment"
	@echo ""
	@echo "Development Commands:"
	@echo "  install        - Install Python dependencies"
	@echo "  test           - Run tests"
	@echo "  lint           - Run linting"
	@echo "  format         - Format code"
	@echo "  clean          - Clean all environments"

# Installation
install:
	pip install -r requirements.txt
	pip install -r demo/requirements.txt
	pip install -r production/requirements.txt

# Demo Commands
demo-setup:
	@echo "Setting up demo environment..."
	cd demo && docker-compose pull
	cd demo && docker-compose build

demo-start:
	@echo "Starting demo services..."
	cd demo && docker-compose up -d
	@echo "Waiting for services to start..."
	sleep 30
	@echo "Demo services started. Access:"
	@echo "  Health: http://localhost:8080/health"
	@echo "  Metrics: http://localhost:9090/metrics"
	@echo "  Flink UI: http://localhost:8081"

demo-stop:
	@echo "Stopping demo services..."
	cd demo && docker-compose down

demo-logs:
	@echo "Viewing demo logs..."
	cd demo && docker-compose logs -f

demo-clean:
	@echo "Cleaning demo environment..."
	cd demo && docker-compose down -v --rmi all

# Production Commands
prod-build:
	@echo "Building production Docker image..."
	docker build -f production/deployment/Dockerfile -t postgres-starrocks-sync:latest .

prod-deploy:
	@echo "Deploying production environment (Docker Compose)..."
	cd production/deployment && chmod +x scripts/deploy.sh
	cd production/deployment && ./scripts/deploy.sh docker

prod-k8s:
	@echo "Deploying production environment (Kubernetes)..."
	cd production/deployment && chmod +x scripts/deploy.sh
	cd production/deployment && ./scripts/deploy.sh k8s

prod-stop:
	@echo "Stopping production services..."
	cd production/deployment && docker-compose down

prod-logs:
	@echo "Viewing production logs..."
	cd production/deployment && docker-compose logs -f

prod-clean:
	@echo "Cleaning production environment..."
	cd production/deployment && docker-compose down -v --rmi all

# Development Commands
test:
	@echo "Running tests..."
	python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

lint:
	@echo "Running linting..."
	flake8 src/ tests/
	mypy src/

format:
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/

# Clean all
clean: demo-clean prod-clean
	@echo "Cleaning all environments..."
	docker system prune -f
	docker volume prune -f

# Health checks
health-demo:
	@echo "Checking demo health..."
	curl -f http://localhost:8080/health || echo "Demo not running"

health-prod:
	@echo "Checking production health..."
	curl -f http://localhost:8080/health || echo "Production not running"

# Monitoring
monitor-demo:
	@echo "Opening demo monitoring..."
	@echo "Health: http://localhost:8080/health"
	@echo "Metrics: http://localhost:9090/metrics"
	@echo "Flink UI: http://localhost:8081"
	@echo "Grafana: http://localhost:3000 (admin/admin)"

monitor-prod:
	@echo "Opening production monitoring..."
	@echo "Health: http://localhost:8080/health"
	@echo "Metrics: http://localhost:9090/metrics"
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3000"

# Database operations
db-reset-demo:
	@echo "Resetting demo database..."
	cd demo && docker-compose down -v
	cd demo && docker-compose up -d
	sleep 30
	@echo "Demo database reset complete"

db-backup-demo:
	@echo "Backing up demo database..."
	docker exec demo_postgres pg_dump -U demo_user demo_db > demo_backup.sql
	@echo "Demo database backed up to demo_backup.sql"

# Configuration
config-validate:
	@echo "Validating configurations..."
	python -c "from demo.src.config_manager import ConfigManager; import yaml; config = yaml.safe_load(open('demo/config/demo_config.yaml')); ConfigManager(config); print('Demo config valid')"
	python -c "from production.src.config_manager import ProductionConfigManager; config = ProductionConfigManager(); print('Production config valid')"

# Documentation
docs-serve:
	@echo "Serving documentation..."
	@echo "Documentation available in docs/ directory"
	@echo "Open docs/README.md for main documentation"

# Quick start
quick-demo: demo-setup demo-start
	@echo "Demo environment ready!"
	@make monitor-demo

quick-prod: prod-build prod-deploy
	@echo "Production environment ready!"
	@make monitor-prod
