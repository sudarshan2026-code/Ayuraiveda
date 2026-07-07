const { authMiddleware } = require('../../middleware/auth');
const db = require('../../lib/db');

const handler = async (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const userId = req.user.id;

    // Get user details
    const userResult = await db.query(
      'SELECT id, name, email, phone, role, profile_image, created_at FROM users WHERE id = $1',
      [userId]
    );

    if (userResult.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = userResult.rows[0];

    // Get role-specific profile
    let profile = null;
    if (user.role === 'user') {
      const profileResult = await db.query(
        'SELECT * FROM user_profiles WHERE user_id = $1',
        [userId]
      );
      profile = profileResult.rows[0];
    } else if (user.role === 'doctor') {
      const profileResult = await db.query(
        'SELECT * FROM doctor_profiles WHERE user_id = $1',
        [userId]
      );
      profile = profileResult.rows[0];
    } else if (user.role === 'college') {
      const profileResult = await db.query(
        'SELECT * FROM college_profiles WHERE user_id = $1',
        [userId]
      );
      profile = profileResult.rows[0];
    }

    // Get subscription status
    const subscriptionResult = await db.query(
      'SELECT status, start_date, end_date FROM subscriptions WHERE user_id = $1 AND status = $2 ORDER BY created_at DESC LIMIT 1',
      [userId, 'active']
    );

    const subscription = subscriptionResult.rows[0] || null;

    res.status(200).json({
      success: true,
      user,
      profile,
      subscription
    });
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({ error: 'Failed to get user data' });
  }
};

module.exports = authMiddleware(handler);
