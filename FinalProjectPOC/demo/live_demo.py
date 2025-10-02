#!/usr/bin/env python3
"""
Live Demo Script for PostgreSQL to StarRocks Real-time Data Sync
This script provides an interactive demo with real-time monitoring.
"""

import os
import sys
import time
import psycopg2
import pymysql
from datetime import datetime
from typing import Dict, Any, List
import yaml
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from config_manager import ConfigManager

class LiveDemo:
    """Live demo class for real-time data sync monitoring."""
    
    def __init__(self):
        """Initialize the live demo."""
        self.config = self.load_config()
        self.config_manager = ConfigManager(self.config)
        self.postgres_config = self.config_manager.get_postgres_config()
        self.starrocks_config = self.config_manager.get_starrocks_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_path = Path(__file__).parent / "config" / "demo_config.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        # Override Docker service names with localhost for external access
        config['postgres']['host'] = 'localhost'
        config['starrocks']['host'] = 'localhost'
        config['starrocks']['port'] = 3307  # External port mapping
        
        return config
    
    def get_postgres_connection(self):
        """Get PostgreSQL connection."""
        return psycopg2.connect(
            host=self.postgres_config.host,
            port=self.postgres_config.port,
            database=self.postgres_config.database,
            user=self.postgres_config.username,
            password=self.postgres_config.password,
            connect_timeout=5
        )
    
    def get_starrocks_connection(self):
        """Get StarRocks (MySQL) connection."""
        return pymysql.connect(
            host=self.starrocks_config.host,
            port=self.starrocks_config.port,
            database=self.starrocks_config.database,
            user=self.starrocks_config.username,
            password=self.starrocks_config.password,
            connect_timeout=5
        )
    
    def test_connections(self) -> Dict[str, bool]:
        """Test database connections."""
        results = {'postgres': False, 'starrocks': False}
        
        # Test PostgreSQL
        try:
            with self.get_postgres_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    results['postgres'] = True
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
        
        # Test StarRocks
        try:
            with self.get_starrocks_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    results['starrocks'] = True
        except Exception as e:
            print(f"❌ StarRocks connection failed: {e}")
        
        return results
    
    def get_data_counts(self) -> Dict[str, Dict[str, int]]:
        """Get current data counts from both databases."""
        counts = {
            'postgres': {'users': 0, 'orders': 0},
            'starrocks': {'users': 0, 'orders': 0}
        }
        
        try:
            # Get PostgreSQL counts
            with self.get_postgres_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM users")
                    counts['postgres']['users'] = cursor.fetchone()[0]
                    cursor.execute("SELECT COUNT(*) FROM orders")
                    counts['postgres']['orders'] = cursor.fetchone()[0]
        except Exception as e:
            print(f"❌ PostgreSQL connection error: {e}")
        
        try:
            # Get StarRocks counts
            with self.get_starrocks_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM users")
                    counts['starrocks']['users'] = cursor.fetchone()[0]
                    cursor.execute("SELECT COUNT(*) FROM orders")
                    counts['starrocks']['orders'] = cursor.fetchone()[0]
        except Exception as e:
            print(f"❌ StarRocks connection error: {e}")
        
        return counts
    
    def display_status(self, counts: Dict[str, Dict[str, int]]):
        """Display current sync status."""
        print("\n" + "="*60)
        print("🔄 REAL-TIME DATA SYNC STATUS")
        print("="*60)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # PostgreSQL Status
        print("📊 POSTGRESQL (Source):")
        print(f"   👥 Users: {counts['postgres']['users']}")
        print(f"   🛒 Orders: {counts['postgres']['orders']}")
        print()
        
        # StarRocks Status
        print("🎯 STARROCKS (Target):")
        print(f"   👥 Users: {counts['starrocks']['users']}")
        print(f"   🛒 Orders: {counts['starrocks']['orders']}")
        print()
        
        # Sync Status
        users_synced = counts['postgres']['users'] == counts['starrocks']['users']
        orders_synced = counts['postgres']['orders'] == counts['starrocks']['orders']
        
        if users_synced and orders_synced:
            print("✅ SYNC STATUS: FULLY SYNCHRONIZED")
        else:
            print("⚠️  SYNC STATUS: PENDING SYNC")
            if not users_synced:
                print(f"   - Users: {counts['postgres']['users']} → {counts['starrocks']['users']}")
            if not orders_synced:
                print(f"   - Orders: {counts['postgres']['orders']} → {counts['starrocks']['orders']}")
        
        print("="*60)
    
    def add_test_data(self, table: str, data: Dict[str, Any]):
        """Add test data to PostgreSQL."""
        try:
            with self.get_postgres_connection() as conn:
                with conn.cursor() as cursor:
                    if table == 'users':
                        cursor.execute(
                            "INSERT INTO users (username, email, created_at, updated_at) VALUES (%s, %s, %s, %s)",
                            (data['username'], data['email'], data['created_at'], data['updated_at'])
                        )
                    elif table == 'orders':
                        cursor.execute(
                            "INSERT INTO orders (user_id, product_name, quantity, price, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (data['user_id'], data['product_name'], data['quantity'], data['price'], data['status'], data['created_at'], data['updated_at'])
                        )
                    conn.commit()
                    print(f"✅ Added new {table} data: {data}")
        except Exception as e:
            print(f"❌ Error adding data: {e}")
    
    def show_recent_data(self, table: str, limit: int = 3):
        """Show recent data from both databases."""
        print(f"\n📋 RECENT {table.upper()} DATA:")
        print("-" * 40)
        
        try:
            # PostgreSQL data
            with self.get_postgres_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT {limit}")
                    pg_data = cursor.fetchall()
                    print("PostgreSQL (Source):")
                    for row in pg_data:
                        print(f"  {row}")
        except Exception as e:
            print(f"❌ PostgreSQL error: {e}")
        
        try:
            # StarRocks data
            with self.get_starrocks_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT {limit}")
                    sr_data = cursor.fetchall()
                    print("StarRocks (Target):")
                    for row in sr_data:
                        print(f"  {row}")
        except Exception as e:
            print(f"❌ StarRocks error: {e}")
    
    def run_live_monitoring(self, duration_minutes: int = 5):
        """Run live monitoring for specified duration."""
        print("🚀 STARTING LIVE DATA SYNC MONITORING")
        print(f"⏱️  Duration: {duration_minutes} minutes")
        print("Press Ctrl+C to stop early")
        print()
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        try:
            while time.time() < end_time:
                counts = self.get_data_counts()
                self.display_status(counts)
                
                # Wait 10 seconds before next check
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
    
    def interactive_demo(self):
        """Run interactive demo with menu options."""
        while True:
            print("\n" + "="*60)
            print("🎬 POSTGRESQL TO STARROCKS LIVE DEMO")
            print("="*60)
            print("1. 📊 Show Current Sync Status")
            print("2. 🔄 Start Live Monitoring (5 minutes)")
            print("3. ➕ Add Test User Data")
            print("4. ➕ Add Test Order Data")
            print("5. 📋 Show Recent Users Data")
            print("6. 📋 Show Recent Orders Data")
            print("7. 🔍 Check Database Connections")
            print("8. ❌ Exit")
            print("="*60)
            
            choice = input("Select an option (1-8): ").strip()
            
            if choice == '1':
                counts = self.get_data_counts()
                self.display_status(counts)
                
            elif choice == '2':
                self.run_live_monitoring(5)
                
            elif choice == '3':
                username = input("Enter username: ").strip()
                email = input("Enter email: ").strip()
                now = datetime.now()
                self.add_test_data('users', {
                    'username': username,
                    'email': email,
                    'created_at': now,
                    'updated_at': now
                })
                
            elif choice == '4':
                user_id = int(input("Enter user_id: "))
                product = input("Enter product name: ").strip()
                quantity = int(input("Enter quantity: "))
                price = float(input("Enter price: "))
                status = input("Enter status: ").strip()
                now = datetime.now()
                self.add_test_data('orders', {
                    'user_id': user_id,
                    'product_name': product,
                    'quantity': quantity,
                    'price': price,
                    'status': status,
                    'created_at': now,
                    'updated_at': now
                })
                
            elif choice == '5':
                self.show_recent_data('users')
                
            elif choice == '6':
                self.show_recent_data('orders')
                
            elif choice == '7':
                print("🔍 Testing Database Connections...")
                results = self.test_connections()
                
                if results['postgres']:
                    print("✅ PostgreSQL connection: OK")
                else:
                    print("❌ PostgreSQL connection: FAILED")
                
                if results['starrocks']:
                    print("✅ StarRocks connection: OK")
                else:
                    print("❌ StarRocks connection: FAILED")
                
                if not results['postgres'] or not results['starrocks']:
                    print("\n💡 Troubleshooting Tips:")
                    print("1. Make sure Docker services are running: docker-compose ps")
                    print("2. Start services if needed: docker-compose up -d")
                    print("3. Wait 30 seconds for services to fully start")
                    print("4. Check port mappings: PostgreSQL (5432), StarRocks (3307)")
                    
            elif choice == '8':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option. Please try again.")
            
            input("\nPress Enter to continue...")

def main():
    """Main entry point for the live demo."""
    try:
        demo = LiveDemo()
        demo.interactive_demo()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
