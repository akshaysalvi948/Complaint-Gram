# PostgreSQL to StarRocks Live Demo Launcher
Write-Host "Starting PostgreSQL to StarRocks Live Demo..." -ForegroundColor Green
Write-Host ""

# Check if Docker is running
try {
    docker ps | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
} catch {
    Write-Host "ERROR: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if demo services are running
$services = docker-compose ps --services --filter "status=running"
if ($services.Count -lt 5) {
    Write-Host "Starting demo services..." -ForegroundColor Yellow
    docker-compose up -d
    Write-Host "Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
}

Write-Host ""
Write-Host "Starting Live Demo Python Script..." -ForegroundColor Green
Write-Host ""

# Run the live demo
python live_demo.py

Read-Host "Press Enter to exit"
