#!/usr/bin/env python3
"""
Demo application for PostgreSQL to StarRocks real-time data sync.
This is a simple 2x2 table demo implementation with basic monitoring.
"""

import os
import sys
import yaml
import logging
import time
import threading
from pathlib import Path
from typing import Dict, Any, List
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import psycopg2
import pymysql
from datetime import datetime

# Add src to Python path
sys.path.append(str(Path(__file__).parent))

from config_manager import ConfigManager
from logger_setup import setup_logging

logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP handler for health checks."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            health_data = {
                "status": "healthy",
                "timestamp": time.time(),
                "service": "postgres-starrocks-sync-demo",
                "version": "1.0.0"
            }
            
            self.wfile.write(json.dumps(health_data).encode())
        elif self.path == '/health/ready':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ready"}).encode())
        elif self.path == '/health/live':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "alive"}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def start_health_server(port: int = 8080):
    """Start the health check HTTP server."""
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        logger.info(f"Health check server started on port {port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"Failed to start health server: {e}")


def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    config_path = Path(__file__).parent.parent / "config" / "demo_config.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def simulate_data_sync(config_manager: ConfigManager):
    """Simulate data synchronization process."""
    logger.info("Starting data synchronization simulation...")
    
    tables = config_manager.get_all_tables()
    logger.info(f"Configured tables: {[table.source_table for table in tables]}")
    
    # Simulate sync process
    sync_count = 0
    while True:
        try:
            for table in tables:
                logger.info(f"Syncing table: {table.source_table} -> {table.target_table}")
                
                # Simulate actual data sync
                sync_table_data(table, config_manager)
                
                sync_count += 1
                
                if sync_count % 10 == 0:
                    logger.info(f"Processed {sync_count} sync operations")
            
            # Wait before next sync cycle
            time.sleep(30)
            
        except KeyboardInterrupt:
            logger.info("Sync simulation interrupted")
            break
        except Exception as e:
            logger.error(f"Error in sync simulation: {e}")
            time.sleep(5)


def sync_table_data(table_config, config_manager):
    """Sync data from PostgreSQL to target database."""
    try:
        # Get database configurations
        postgres_config = config_manager.get_postgres_config()
        starrocks_config = config_manager.get_starrocks_config()
        
        logger.info(f"Syncing {table_config.source_table} -> {table_config.target_table}")
        logger.info(f"Source: PostgreSQL ({postgres_config.host}:{postgres_config.port})")
        logger.info(f"Target: StarRocks ({starrocks_config.host}:{starrocks_config.port})")
        
        # Connect to PostgreSQL
        postgres_conn = psycopg2.connect(
            host=postgres_config.host,
            port=postgres_config.port,
            database=postgres_config.database,
            user=postgres_config.username,
            password=postgres_config.password
        )
        
        # Connect to StarRocks (MySQL)
        starrocks_conn = pymysql.connect(
            host=starrocks_config.host,
            port=starrocks_config.port,
            database=starrocks_config.database,
            user=starrocks_config.username,
            password=starrocks_config.password
        )
        
        try:
            # Get data from PostgreSQL
            with postgres_conn.cursor() as pg_cursor:
                pg_cursor.execute(f"SELECT * FROM {table_config.source_table}")
                rows = pg_cursor.fetchall()
                
                # Get column names
                column_names = [desc[0] for desc in pg_cursor.description]
                
                logger.info(f"Found {len(rows)} rows in {table_config.source_table}")
                
                if rows:
                    # Clear existing data in target table (for demo purposes)
                    with starrocks_conn.cursor() as sr_cursor:
                        sr_cursor.execute(f"DELETE FROM {table_config.target_table}")
                        logger.info(f"Cleared existing data from {table_config.target_table}")
                        
                        # Insert data into StarRocks
                        placeholders = ', '.join(['%s'] * len(column_names))
                        columns = ', '.join(column_names)
                        
                        insert_query = f"INSERT INTO {table_config.target_table} ({columns}) VALUES ({placeholders})"
                        sr_cursor.executemany(insert_query, rows)
                        starrocks_conn.commit()
                        
                        logger.info(f"Successfully synced {len(rows)} rows to {table_config.target_table}")
                        
                        # Log sample data
                        if len(rows) > 0:
                            logger.info(f"Sample data: {rows[0]}")
                
        finally:
            postgres_conn.close()
            starrocks_conn.close()
        
        logger.info(f"Data sync completed for {table_config.source_table}")
        
    except Exception as e:
        logger.error(f"Error syncing {table_config.source_table}: {e}")
        raise


def main():
    """Main entry point for the demo application."""
    try:
        # Setup logging
        setup_logging()
        logger.info("Starting PostgreSQL to StarRocks Demo Sync")
        
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded successfully")
        
        # Initialize config manager
        config_manager = ConfigManager(config)
        
        # Start health check server in a separate thread
        health_thread = threading.Thread(target=start_health_server, daemon=True)
        health_thread.start()
        
        # Start sync simulation
        logger.info("Starting data synchronization simulation...")
        simulate_data_sync(config_manager)
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Application failed with error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
