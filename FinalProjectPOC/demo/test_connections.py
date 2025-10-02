#!/usr/bin/env python3
"""
Quick connection test for the live demo
"""

import psycopg2
import pymysql

def test_postgres():
    """Test PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='demo_db',
            user='demo_user',
            password='demo_password',
            connect_timeout=5
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"✅ PostgreSQL: Connected successfully, {count} users found")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL: Connection failed - {e}")
        return False

def test_starrocks():
    """Test StarRocks (MySQL) connection."""
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3307,
            database='demo_db',
            user='root',
            password='root',
            connect_timeout=5
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"✅ StarRocks: Connected successfully, {count} users found")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ StarRocks: Connection failed - {e}")
        return False

def main():
    print("🔍 Testing Database Connections...")
    print("=" * 40)
    
    pg_ok = test_postgres()
    sr_ok = test_starrocks()
    
    print("=" * 40)
    if pg_ok and sr_ok:
        print("🎉 All connections successful! You can run the live demo now.")
        print("Run: python live_demo.py")
    else:
        print("❌ Some connections failed. Check Docker services are running.")
        print("Run: docker-compose ps")

if __name__ == "__main__":
    main()
