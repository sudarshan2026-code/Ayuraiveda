const bcrypt = require('bcrypt');
const db = require('../lib/db');

async function createAdminUser() {
  try {
    const email = 'anantalabsindia@gmail.com';
    const password = 'A@L!2026#Secure';
    const name = 'Admin';

    const existingAdmin = await db.query(
      'SELECT id FROM users WHERE email = $1',
      [email]
    );

    if (existingAdmin.rows.length > 0) {
      console.log('✅ Admin user already exists');
      console.log('Email:', email);
      console.log('Password:', password);
      process.exit(0);
    }

    const passwordHash = await bcrypt.hash(password, 10);

    // Insert admin only in users table with role='admin'
    await db.query(
      'INSERT INTO users (name, email, password_hash, role) VALUES ($1, $2, $3, $4)',
      [name, email, passwordHash, 'admin']
    );

    console.log('✅ Admin user created successfully in users table');
    console.log('📧 Email:', email);
    console.log('🔑 Password:', password);
    console.log('👤 Role: admin');
    console.log('\n⚠️  Admin credentials are stored ONLY in users table');
    console.log('No separate admin table - admin is identified by role="admin"');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ Error creating admin user:', error);
    process.exit(1);
  }
}

createAdminUser();
