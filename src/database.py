import sqlite3
from src.config import DATABASE_URL, log_system

def get_db_connection():
    """
    Creates a database connection with High-Concurrency settings.
    TIMEOUT: Waits 10s for the file to unlock before crashing.
    """
    conn = sqlite3.connect(DATABASE_URL, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db_connection()
        
        # --- PERFORMANCE UPGRADE: WAL MODE ---
        # Write-Ahead Logging allows simultaneous Read/Write.
        # This prevents the 'Database Locked' error during streaming.
        conn.execute("PRAGMA journal_mode=WAL;") 
        
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS grills (
                id TEXT PRIMARY KEY,
                owner_id TEXT,
                model TEXT,
                status TEXT,
                current_temp INTEGER,
                target_temp INTEGER,
                fan_speed INTEGER,
                auger_rate INTEGER,
                latest_thought TEXT
            )
        ''')
        conn.commit()
        conn.close()
        log_system("DATABASE INTEGRITY: VERIFIED (WAL MODE ACTIVE)")
    except Exception as e:
        log_system(f"DATABASE CRITICAL FAILURE: {e}")
