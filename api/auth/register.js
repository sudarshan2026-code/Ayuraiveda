const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const db = require('../../lib/db');
const { sendWelcomeEmail } = require('../../lib/email');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { name, email, password, phone, role } = req.body;

    // Validation
    if (!name || !email || !password || !role) {
      return res.status(400).json({ error: 'All fields are required' });
    }

    if (!['user', 'doctor', 'college'].includes(role)) {
      return res.status(400).json({ error: 'Invalid role' });
    }

    // Check if user exists
    const existingUser = await db.query(
      'SELECT id FROM users WHERE email = $1',
      [email]
    );

    if (existingUser.rows.length > 0) {
      return res.status(400).json({ error: 'Email already registered' });
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, 10);

    // Create user
    const userResult = await db.query(
      'INSERT INTO users (name, email, password_hash, phone, role) VALUES ($1, $2, $3, $4, $5) RETURNING id, name, email, role',
      [name, email, passwordHash, phone, role]
    );

    const user = userResult.rows[0];

    // Create role-specific profile
    if (role === 'user') {
      await db.query(
        'INSERT INTO user_profiles (user_id) VALUES ($1)',
        [user.id]
      );
    } else if (role === 'doctor') {
      await db.query(
        'INSERT INTO doctor_profiles (user_id) VALUES ($1)',
        [user.id]
      );
    } else if (role === 'college') {
      await db.query(
        'INSERT INTO college_profiles (user_id) VALUES ($1)',
        [user.id]
      );
    }

    // Send welcome email
    await sendWelcomeEmail(email, name, role);

    // Generate JWT token
    const token = jwt.sign(
      { id: user.id, email: user.email, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.status(201).json({
      success: true,
      message: 'Registration successful',
      token,
      user: {
        id: user.id,
        name: user.name,
        email: user.email,
        role: user.role
      }
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Registration failed' });
  }
};
