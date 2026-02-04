import sqlite3
import datetime
from utils.config import Config
import os
import json

class DatabaseManager:
    def __init__(self):
        self.db_path = Config.DB_PATH
        self.use_cloud = Config.USE_CLOUD
        self.supabase = None
        
        self.init_local_db()
        self.init_cloud_db()

    def init_local_db(self):
        """Initialize SQLite database with required tables."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                employee_id TEXT UNIQUE NOT NULL,
                face_encoding TEXT, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Attendance Logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                synced BOOLEAN DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def init_cloud_db(self):
        """Initialize Supabase client if enabled."""
        if self.use_cloud and Config.SUPABASE_URL and Config.SUPABASE_KEY:
            try:
                from supabase import create_client
                self.supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
                print("Connected to Supabase Cloud.")
            except Exception as e:
                print(f"Failed to connect to Supabase: {e}")
                self.use_cloud = False

    def add_user_placeholder(self, name, employee_id):
        """Creates a user entry and returns the ID for training."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if exists
            cursor.execute("SELECT id FROM users WHERE employee_id = ?", (employee_id,))
            exists = cursor.fetchone()
            if exists:
                conn.close()
                return False, "Employee ID already exists"
                
            cursor.execute("INSERT INTO users (name, employee_id) VALUES (?, ?)", (name, employee_id))
            new_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True, new_id
        except Exception as e:
            return False, str(e)

    def get_all_users(self):
        """Retrieve all users."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def log_attendance(self, user_id, name):
        """Log attendance with cooldown check."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if already logged TODAY
        # We use 'localtime' to ensure day boundaries are correct for the user
        cursor.execute('''
            SELECT timestamp FROM attendance 
            WHERE user_id = ? AND date(timestamp) = date('now', 'localtime')
            ORDER BY timestamp DESC LIMIT 1
        ''', (user_id,))
        
        last_log = cursor.fetchone()
        
        if last_log:
            conn.close()
            # It's already done today.
            # We return False and the specific message.
            return False, "You already took attendance today"
        
        # If not, log it
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO attendance (user_id, name, timestamp) VALUES (?, ?, ?)",
                       (user_id, name, now_str))
        conn.commit()
        
        # Trigger cloud sync in background
        if self.use_cloud:
            self.sync_to_cloud(user_id, name)
            
        conn.close()
        return True, f"Welcome, {name}! Marked Present."

    def sync_to_cloud(self, user_id, name):
        """Push log to Supabase."""
        try:
            data = {
                "user_id": user_id,
                "name": name,
                "timestamp": datetime.datetime.now().isoformat()
            }
            self.supabase.table("attendance").insert(data).execute()
        except Exception as e:
            print(f"Cloud sync failed: {e}")

    def get_recent_logs(self, limit=10):
        """Get recent attendance logs."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, timestamp FROM attendance ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_stats(self):
        """Get basic stats."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE date(timestamp) = date('now', 'localtime')")
        today_attendance = cursor.fetchone()[0]
        
        conn.close()
        return {"users": total_users, "today": today_attendance}
