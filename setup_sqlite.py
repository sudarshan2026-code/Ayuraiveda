import sqlite3
import bcrypt
import os

DB_PATH = 'ananta_labs.db'

def create_tables():
    """Create all required tables in SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Create users table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                phone TEXT,
                role TEXT NOT NULL CHECK (role IN ('user', 'doctor', 'college', 'admin')),
                profile_image TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_profiles table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                age INTEGER,
                gender TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                pincode TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Create doctor_profiles table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS doctor_profiles (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                qualification TEXT,
                specialization TEXT,
                registration_number TEXT,
                clinic_name TEXT,
                clinic_address TEXT,
                experience_years INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Create college_profiles table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS college_profiles (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                college_name TEXT,
                college_code TEXT,
                university TEXT,
                address TEXT,
                contact_person TEXT,
                designation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Create subscriptions table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                plan_type TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('active', 'expired', 'cancelled')),
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP NOT NULL,
                amount REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Create orders table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                order_id TEXT UNIQUE NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Create payments table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id TEXT PRIMARY KEY,
                order_id TEXT,
                payment_id TEXT UNIQUE NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                payment_gateway TEXT,
                transaction_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
            )
        ''')
        
        # Create reports table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                report_type TEXT NOT NULL,
                report_data TEXT,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Create indexes
        cur.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)')
        
        conn.commit()
        cur.close()
        conn.close()
        
        print('✅ All tables created successfully')
        return True
    except Exception as e:
        print(f'❌ Error creating tables: {str(e)}')
        return False

def create_admin_user():
    """Create the admin user"""
    try:
        import uuid
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Check if admin exists
        cur.execute("SELECT id FROM users WHERE email = 'anantalabsindia@gmail.com'")
        if cur.fetchone():
            print('ℹ️ Admin user already exists')
            cur.close()
            conn.close()
            return True
        
        # Create admin user
        password_hash = bcrypt.hashpw('A@L!2026#Secure'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO users (id, name, email, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            (admin_id, 'Ananta Labs Admin', 'anantalabsindia@gmail.com', password_hash, 'admin')
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        print('✅ Admin user created successfully')
        print('   Email: anantalabsindia@gmail.com')
        print('   Password: A@L!2026#Secure')
        return True
    except Exception as e:
        print(f'❌ Error creating admin user: {str(e)}')
        return False

if __name__ == '__main__':
    print('🚀 Starting SQLite database setup...\n')
    
    if create_tables():
        create_admin_user()
        print(f'\n✅ Database setup completed successfully!')
        print(f'📁 Database file: {os.path.abspath(DB_PATH)}')
    else:
        print('\n❌ Failed to create tables')
