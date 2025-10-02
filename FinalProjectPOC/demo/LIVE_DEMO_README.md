# 🎬 Live Demo - PostgreSQL to StarRocks Real-time Data Sync

This live demo provides an interactive interface to monitor and test real-time data synchronization between PostgreSQL and StarRocks.

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)
```bash
python start_demo.py
```

### Option 2: Manual Startup
```bash
# 1. Start services
docker-compose up -d

# 2. Wait for services to start (30 seconds)
# 3. Run live demo
python live_demo.py
```

### Option 3: Test Connections First
```bash
python test_connections.py
python live_demo.py
```

## 📋 Live Demo Features

### Interactive Menu Options:
1. **📊 Show Current Sync Status** - Display data counts and sync status
2. **🔄 Start Live Monitoring** - Real-time monitoring for 5 minutes
3. **➕ Add Test User Data** - Add new users to PostgreSQL
4. **➕ Add Test Order Data** - Add new orders to PostgreSQL
5. **📋 Show Recent Users Data** - View recent users from both databases
6. **📋 Show Recent Orders Data** - View recent orders from both databases
7. **🔍 Check Database Connections** - Test connectivity
8. **❌ Exit** - Exit the demo

## 🔧 Troubleshooting

### Connection Issues
If you get connection errors:

1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Check services are running:**
   ```bash
   docker-compose ps
   ```

3. **Start services if needed:**
   ```bash
   docker-compose up -d
   ```

4. **Wait for services to start:**
   ```bash
   # Wait 30 seconds after starting services
   ```

### Port Mappings
- **PostgreSQL:** localhost:5432
- **StarRocks (MySQL):** localhost:3307
- **Flink UI:** http://localhost:8081
- **Sync App Health:** http://localhost:8080/health

## 📊 Demo Scenarios

### Scenario 1: Monitor Existing Sync
1. Run `python live_demo.py`
2. Select option 1 to see current status
3. Select option 2 to start live monitoring
4. Watch the sync process in real-time

### Scenario 2: Add New Data and Watch Sync
1. Run `python live_demo.py`
2. Select option 3 to add a new user
3. Select option 4 to add a new order
4. Select option 2 to monitor the sync
5. Watch new data appear in StarRocks

### Scenario 3: Compare Data Between Databases
1. Run `python live_demo.py`
2. Select option 5 to see recent users
3. Select option 6 to see recent orders
4. Verify data is identical in both databases

## 🎯 What You'll See

### Sync Status Display
```
============================================================
🔄 REAL-TIME DATA SYNC STATUS
============================================================
⏰ Time: 2025-09-26 18:30:15

📊 POSTGRESQL (Source):
   👥 Users: 14
   🛒 Orders: 15

🎯 STARROCKS (Target):
   👥 Users: 14
   🛒 Orders: 15

✅ SYNC STATUS: FULLY SYNCHRONIZED
============================================================
```

### Live Monitoring Output
```
🔄 REAL-TIME DATA SYNC STATUS
============================================================
⏰ Time: 2025-09-26 18:30:15

📊 POSTGRESQL (Source):
   👥 Users: 15
   🛒 Orders: 16

🎯 STARROCKS (Target):
   👥 Users: 14
   🛒 Orders: 15

⚠️  SYNC STATUS: PENDING SYNC
   - Users: 15 → 14
   - Orders: 16 → 15
============================================================
```

## 🔍 Technical Details

### Real-time Sync Process
- **Sync Frequency:** Every 30 seconds
- **Sync Method:** Full table sync (clear + insert)
- **Data Flow:** PostgreSQL → StarRocks (MySQL)
- **Monitoring:** Live logs and status updates

### Database Schema
**Users Table:**
- id (INT PRIMARY KEY)
- username (VARCHAR)
- email (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

**Orders Table:**
- id (INT PRIMARY KEY)
- user_id (INT)
- product_name (VARCHAR)
- quantity (INT)
- price (DECIMAL)
- status (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

## 🎉 Success Indicators

✅ **Fully Synchronized:** User and order counts match between databases
✅ **Real-time Updates:** New data appears in StarRocks within 30 seconds
✅ **Data Integrity:** All data fields are correctly transferred
✅ **Live Monitoring:** Status updates show sync progress

## 🛠️ Advanced Usage

### Custom Monitoring Duration
Modify the `run_live_monitoring()` method to change duration:
```python
self.run_live_monitoring(10)  # 10 minutes instead of 5
```

### Add Custom Test Data
Use the interactive menu options 3 and 4 to add custom data and watch it sync.

### View Sync Logs
```bash
docker logs -f demo_sync_app
```

## 📝 Notes

- The demo uses MySQL as a StarRocks substitute for easier setup
- Real production would use actual StarRocks with Flink CDC
- The sync process runs continuously in the background
- All data changes are logged for monitoring

---

**Ready to start? Run: `python live_demo.py`** 🚀
