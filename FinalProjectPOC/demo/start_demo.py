#!/usr/bin/env python3
"""
Demo Startup Script - Ensures services are running before starting live demo
"""

import subprocess
import time
import sys
from pathlib import Path

def run_command(command, shell=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_docker_running():
    """Check if Docker is running."""
    success, stdout, stderr = run_command("docker ps")
    if not success:
        print("❌ Docker is not running. Please start Docker Desktop first.")
        return False
    return True

def check_services_running():
    """Check if demo services are running."""
    success, stdout, stderr = run_command("docker-compose ps")
    if not success:
        return False
    
    # Count running services
    running_services = [line for line in stdout.split('\n') if 'Up' in line]
    return len(running_services) >= 5

def start_services():
    """Start demo services."""
    print("🚀 Starting demo services...")
    success, stdout, stderr = run_command("docker-compose up -d")
    if not success:
        print(f"❌ Failed to start services: {stderr}")
        return False
    
    print("⏳ Waiting for services to start (30 seconds)...")
    time.sleep(30)
    return True

def main():
    """Main startup function."""
    print("=" * 60)
    print("🎬 POSTGRESQL TO STARROCKS DEMO STARTUP")
    print("=" * 60)
    
    # Check Docker
    if not check_docker_running():
        sys.exit(1)
    
    print("✅ Docker is running")
    
    # Check services
    if not check_services_running():
        print("⚠️  Demo services are not running")
        if not start_services():
            sys.exit(1)
    else:
        print("✅ Demo services are already running")
    
    # Final check
    if not check_services_running():
        print("❌ Services failed to start properly")
        sys.exit(1)
    
    print("✅ All services are running")
    print("\n🎯 Starting Live Demo...")
    print("=" * 60)
    
    # Start the live demo
    try:
        import live_demo
        live_demo.main()
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    main()
