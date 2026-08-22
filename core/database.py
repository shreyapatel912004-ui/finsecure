import sqlite3
from pathlib import Path
from config.settings import DATABASE_PATH
from datetime import datetime
from .logger import setup_logger

logger = setup_logger(__name__)

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exposed_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_value TEXT UNIQUE NOT NULL,
                key_type TEXT,
                source TEXT,
                source_url TEXT,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                risk_level TEXT,
                status TEXT DEFAULT 'NEW',
                notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_type TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                keys_found INTEGER,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized")
    
    def add_exposed_key(self, key_value, key_type, source, source_url, risk_level='HIGH'):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO exposed_keys 
                (key_value, key_type, source, source_url, risk_level, status)
                VALUES (?, ?, ?, ?, ?, 'NEW')
            ''', (key_value, key_type, source, source_url, risk_level))
            
            conn.commit()
            conn.close()
            logger.info(f"Key added: {key_value[:10]}...")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Key already exists: {key_value[:10]}...")
            return False
        except Exception as e:
            logger.error(f"Error adding key: {str(e)}")
            return False
    
    def get_all_keys(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM exposed_keys ORDER BY found_at DESC')
        keys = cursor.fetchall()
        conn.close()
        return keys
    
    def update_key_status(self, key_value, status):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE exposed_keys SET status = ? WHERE key_value = ?', (status, key_value))
        conn.commit()
        conn.close()

db = Database()
