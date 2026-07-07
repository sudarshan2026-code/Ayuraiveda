import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# Database configuration
DB_NAME = 'ananta_labs'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f'CREATE DATABASE {DB_NAME}')
            print(f'✅ Database "{DB_NAME}" created successfully')
        else:
            print(f'ℹ️ Database "{DB_NAME}" already exists')
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f'❌ Error creating database: {str(e)}')
        return False

def create_tables():
    """Create all required tables"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        
        # Enable UUID extension
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        
        # Create users table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'doctor', 'college', 'admin')),
                profile_image TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create user_profiles table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                age INTEGER,
                gender VARCHAR(20),
                address TEXT,
                city VARCHAR(100),
                state VARCHAR(100),
                pincode VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create doctor_profiles table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS doctor_profiles (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                qualification VARCHAR(255),
                specialization VARCHAR(255),
                registration_number VARCHAR(100),
                clinic_name VARCHAR(255),
                clinic_address TEXT,
                experience_years INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create college_profiles table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS college_profiles (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                college_name VARCHAR(255),
                college_code VARCHAR(100),
                university VARCHAR(255),
                address TEXT,
                contact_person VARCHAR(255),
                designation VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create subscriptions table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                plan_type VARCHAR(50) NOT NULL,
                status VARCHAR(20) NOT NULL CHECK (status IN ('active', 'expired', 'cancelled')),
                start_date TIMESTAMP NOT NULL,
                end_date TIMESTAMP NOT NULL,
                amount DECIMAL(10, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create orders table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                order_id VARCHAR(100) UNIQUE NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                status VARCHAR(20) NOT NULL,
                payment_method VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create payments table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
                payment_id VARCHAR(100) UNIQUE NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                status VARCHAR(20) NOT NULL,
                payment_gateway VARCHAR(50),
                transaction_id VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create reports table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                report_type VARCHAR(50) NOT NULL,
                report_data JSONB,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        import bcrypt
        
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
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
        cur.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            ('Ananta Labs Admin', 'anantalabsindia@gmail.com', password_hash, 'admin')
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
    print('🚀 Starting database setup...\n')
    
    if create_database():
        if create_tables():
            create_admin_user()
            print('\n✅ Database setup completed successfully!')
        else:
            print('\n❌ Failed to create tables')
    else:
        print('\n❌ Failed to create database')
