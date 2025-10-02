#!/bin/bash

# Production deployment script for PostgreSQL to StarRocks Sync
# This script handles both Docker Compose and Kubernetes deployments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEPLOYMENT_TYPE="${1:-docker}"  # docker or k8s
ENVIRONMENT="${2:-production}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if [ "$DEPLOYMENT_TYPE" = "docker" ]; then
        if ! command -v docker &> /dev/null; then
            log_error "Docker is not installed or not in PATH"
            exit 1
        fi
        
        if ! command -v docker-compose &> /dev/null; then
            log_error "Docker Compose is not installed or not in PATH"
            exit 1
        fi
        
        log_success "Docker and Docker Compose are available"
        
    elif [ "$DEPLOYMENT_TYPE" = "k8s" ]; then
        if ! command -v kubectl &> /dev/null; then
            log_error "kubectl is not installed or not in PATH"
            exit 1
        fi
        
        if ! command -v docker &> /dev/null; then
            log_error "Docker is not installed or not in PATH"
            exit 1
        fi
        
        # Check if kubectl can connect to cluster
        if ! kubectl cluster-info &> /dev/null; then
            log_error "Cannot connect to Kubernetes cluster"
            exit 1
        fi
        
        log_success "kubectl and Docker are available, cluster is accessible"
    fi
}

build_image() {
    log_info "Building Docker image..."
    
    cd "$PROJECT_ROOT"
    
    # Build the production image
    docker build -f production/deployment/Dockerfile -t postgres-starrocks-sync:latest .
    
    if [ $? -eq 0 ]; then
        log_success "Docker image built successfully"
    else
        log_error "Failed to build Docker image"
        exit 1
    fi
}

deploy_docker() {
    log_info "Deploying with Docker Compose..."
    
    cd "$PROJECT_ROOT/production/deployment"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        log_info "Creating .env file from template..."
        cat > .env << EOF
# Database Configuration
POSTGRES_DB=production_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

STARROCKS_DB=production_db
STARROCKS_USER=root
STARROCKS_PASSWORD=root

# Monitoring
GRAFANA_PASSWORD=admin

# Logging
LOG_LEVEL=INFO

# Optional: External services
SENTRY_DSN=
ALERT_WEBHOOK_URL=
SLACK_WEBHOOK=
EOF
        log_success ".env file created"
    fi
    
    # Start services
    log_info "Starting services..."
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        log_success "Services started successfully"
    else
        log_error "Failed to start services"
        exit 1
    fi
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Check service health
    check_docker_health
}

deploy_kubernetes() {
    log_info "Deploying to Kubernetes..."
    
    cd "$PROJECT_ROOT/production/deployment/k8s"
    
    # Create namespace
    log_info "Creating namespace..."
    kubectl apply -f namespace.yaml
    
    # Apply secrets
    log_info "Applying secrets..."
    kubectl apply -f secrets.yaml
    
    # Apply configmaps
    log_info "Applying configmaps..."
    kubectl apply -f configmap.yaml
    
    # Apply PostgreSQL
    log_info "Deploying PostgreSQL..."
    kubectl apply -f postgres.yaml
    
    # Wait for PostgreSQL to be ready
    log_info "Waiting for PostgreSQL to be ready..."
    kubectl wait --for=condition=ready pod -l app=postgres -n postgres-starrocks-sync --timeout=300s
    
    # Apply sync application
    log_info "Deploying sync application..."
    kubectl apply -f sync-app.yaml
    
    # Apply monitoring
    log_info "Deploying monitoring stack..."
    kubectl apply -f monitoring.yaml
    
    # Apply ingress (optional)
    if [ -f ingress.yaml ]; then
        log_info "Applying ingress..."
        kubectl apply -f ingress.yaml
    fi
    
    # Wait for sync app to be ready
    log_info "Waiting for sync application to be ready..."
    kubectl wait --for=condition=ready pod -l app=sync-app -n postgres-starrocks-sync --timeout=300s
    
    log_success "Kubernetes deployment completed"
}

check_docker_health() {
    log_info "Checking service health..."
    
    # Check PostgreSQL
    if docker exec production_postgres pg_isready -U postgres &> /dev/null; then
        log_success "PostgreSQL is healthy"
    else
        log_warning "PostgreSQL health check failed"
    fi
    
    # Check sync app
    if curl -f http://localhost:8080/health &> /dev/null; then
        log_success "Sync application is healthy"
    else
        log_warning "Sync application health check failed"
    fi
    
    # Check Prometheus
    if curl -f http://localhost:9090/-/healthy &> /dev/null; then
        log_success "Prometheus is healthy"
    else
        log_warning "Prometheus health check failed"
    fi
    
    # Check Grafana
    if curl -f http://localhost:3000/api/health &> /dev/null; then
        log_success "Grafana is healthy"
    else
        log_warning "Grafana health check failed"
    fi
}

check_kubernetes_health() {
    log_info "Checking Kubernetes deployment health..."
    
    # Check pods
    kubectl get pods -n postgres-starrocks-sync
    
    # Check services
    kubectl get services -n postgres-starrocks-sync
    
    # Check ingress
    kubectl get ingress -n postgres-starrocks-sync
    
    # Port forward for health checks
    log_info "Setting up port forwarding for health checks..."
    
    # Port forward sync app
    kubectl port-forward -n postgres-starrocks-sync service/sync-app-service 8080:8080 &
    SYNC_PID=$!
    
    # Port forward Prometheus
    kubectl port-forward -n postgres-starrocks-sync service/prometheus-service 9090:9090 &
    PROM_PID=$!
    
    # Port forward Grafana
    kubectl port-forward -n postgres-starrocks-sync service/grafana-service 3000:3000 &
    GRAFANA_PID=$!
    
    # Wait a moment for port forwarding to establish
    sleep 5
    
    # Check health endpoints
    if curl -f http://localhost:8080/health &> /dev/null; then
        log_success "Sync application is healthy"
    else
        log_warning "Sync application health check failed"
    fi
    
    if curl -f http://localhost:9090/-/healthy &> /dev/null; then
        log_success "Prometheus is healthy"
    else
        log_warning "Prometheus health check failed"
    fi
    
    if curl -f http://localhost:3000/api/health &> /dev/null; then
        log_success "Grafana is healthy"
    else
        log_warning "Grafana health check failed"
    fi
    
    # Clean up port forwarding
    kill $SYNC_PID $PROM_PID $GRAFANA_PID 2>/dev/null || true
}

show_access_info() {
    log_info "Deployment completed successfully!"
    echo
    echo "Access Information:"
    echo "=================="
    
    if [ "$DEPLOYMENT_TYPE" = "docker" ]; then
        echo "Sync Application Health: http://localhost:8080/health"
        echo "Sync Application Metrics: http://localhost:9090/metrics"
        echo "Prometheus: http://localhost:9090"
        echo "Grafana: http://localhost:3000 (admin/admin)"
        echo
        echo "To view logs:"
        echo "  docker-compose logs -f sync-app"
        echo
        echo "To stop services:"
        echo "  docker-compose down"
        
    elif [ "$DEPLOYMENT_TYPE" = "k8s" ]; then
        echo "To access services, use port forwarding:"
        echo "  kubectl port-forward -n postgres-starrocks-sync service/sync-app-service 8080:8080"
        echo "  kubectl port-forward -n postgres-starrocks-sync service/prometheus-service 9090:9090"
        echo "  kubectl port-forward -n postgres-starrocks-sync service/grafana-service 3000:3000"
        echo
        echo "Sync Application Health: http://localhost:8080/health"
        echo "Sync Application Metrics: http://localhost:9090/metrics"
        echo "Prometheus: http://localhost:9090"
        echo "Grafana: http://localhost:3000 (admin/admin)"
        echo
        echo "To view logs:"
        echo "  kubectl logs -n postgres-starrocks-sync -l app=sync-app -f"
        echo
        echo "To delete deployment:"
        echo "  kubectl delete namespace postgres-starrocks-sync"
    fi
}

# Main execution
main() {
    log_info "Starting deployment process..."
    log_info "Deployment type: $DEPLOYMENT_TYPE"
    log_info "Environment: $ENVIRONMENT"
    
    check_prerequisites
    build_image
    
    if [ "$DEPLOYMENT_TYPE" = "docker" ]; then
        deploy_docker
        check_docker_health
    elif [ "$DEPLOYMENT_TYPE" = "k8s" ]; then
        deploy_kubernetes
        check_kubernetes_health
    else
        log_error "Invalid deployment type. Use 'docker' or 'k8s'"
        exit 1
    fi
    
    show_access_info
}

# Run main function
main "$@"
