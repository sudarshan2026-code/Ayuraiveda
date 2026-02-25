import sqlite3
from datetime import datetime
import uuid

class ChatDatabase:
    def __init__(self, db_name='ayurveda_chat.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_session(self):
        """Create new chat session"""
        session_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sessions (session_id) VALUES (?)', (session_id,))
        conn.commit()
        conn.close()
        return session_id
    
    def save_message(self, session_id, role, message):
        """Save message to database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (session_id, role, message) 
            VALUES (?, ?, ?)
        ''', (session_id, role, message))
        
        cursor.execute('''
            UPDATE sessions SET last_active = CURRENT_TIMESTAMP 
            WHERE session_id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, session_id, limit=10):
        """Get recent conversation history"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT role, message, timestamp 
            FROM messages 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (session_id, limit))
        
        messages = cursor.fetchall()
        conn.close()
        
        return [{'role': m[0], 'message': m[1], 'timestamp': m[2]} for m in reversed(messages)]
    
    def get_context_for_query(self, session_id, limit=5):
        """Get recent context for better responses"""
        history = self.get_conversation_history(session_id, limit)
        context = []
        for msg in history:
            context.append(f"{msg['role']}: {msg['message']}")
        return "\n".join(context)
    
    def session_exists(self, session_id):
        """Check if session exists"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT session_id FROM sessions WHERE session_id = ?', (session_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
