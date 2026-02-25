import sqlite3
import hashlib
from datetime import datetime
import json

class AuthDatabase:
    def __init__(self, db_path='ayurveda_auth.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            specialization TEXT,
            profile_photo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Assessments table
        c.execute('''CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            patient_name TEXT,
            patient_phone TEXT,
            assessment_data TEXT NOT NULL,
            result_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, email, password, user_type, name, phone=None, specialization=None):
        """Register new user"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO users (email, password, user_type, name, phone, specialization)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (email, self.hash_password(password), user_type, name, phone, specialization))
            conn.commit()
            return True, "Registration successful"
        except sqlite3.IntegrityError:
            return False, "Email already exists"
        finally:
            conn.close()
    
    def login_user(self, email, password):
        """Login user"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                 (email, self.hash_password(password)))
        user = c.fetchone()
        conn.close()
        
        if user:
            return True, {
                'id': user[0],
                'email': user[1],
                'user_type': user[3],
                'name': user[4],
                'phone': user[5],
                'specialization': user[6],
                'profile_photo': user[7]
            }
        return False, None
    
    def get_user(self, user_id):
        """Get user by ID"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'email': user[1],
                'user_type': user[3],
                'name': user[4],
                'phone': user[5],
                'specialization': user[6],
                'profile_photo': user[7]
            }
        return None
    
    def update_profile(self, user_id, name, phone, specialization=None):
        """Update user profile"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''UPDATE users SET name = ?, phone = ?, specialization = ?
                    WHERE id = ?''', (name, phone, specialization, user_id))
        conn.commit()
        conn.close()
    
    def update_profile_photo(self, user_id, photo_path):
        """Update profile photo"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE users SET profile_photo = ? WHERE id = ?', (photo_path, user_id))
        conn.commit()
        conn.close()
    
    def save_assessment(self, user_id, assessment_data, result_data, patient_name=None, patient_phone=None):
        """Save assessment"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO assessments (user_id, patient_name, patient_phone, assessment_data, result_data)
                    VALUES (?, ?, ?, ?, ?)''',
                 (user_id, patient_name, patient_phone, json.dumps(assessment_data), json.dumps(result_data)))
        conn.commit()
        assessment_id = c.lastrowid
        conn.close()
        return assessment_id
    
    def get_user_assessments(self, user_id):
        """Get all assessments for user"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT id, patient_name, patient_phone, assessment_data, result_data, created_at
                    FROM assessments WHERE user_id = ? ORDER BY created_at DESC''', (user_id,))
        assessments = c.fetchall()
        conn.close()
        
        result = []
        for a in assessments:
            result.append({
                'id': a[0],
                'patient_name': a[1],
                'patient_phone': a[2],
                'assessment_data': json.loads(a[3]),
                'result_data': json.loads(a[4]),
                'created_at': a[5]
            })
        return result
    
    def get_assessment(self, assessment_id):
        """Get single assessment"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''SELECT id, user_id, patient_name, patient_phone, assessment_data, result_data, created_at
                    FROM assessments WHERE id = ?''', (assessment_id,))
        a = c.fetchone()
        conn.close()
        
        if a:
            return {
                'id': a[0],
                'user_id': a[1],
                'patient_name': a[2],
                'patient_phone': a[3],
                'assessment_data': json.loads(a[4]),
                'result_data': json.loads(a[5]),
                'created_at': a[6]
            }
        return None
