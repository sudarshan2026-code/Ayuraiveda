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
      'SELECT name, email, role, profile_image FROM users WHERE id = $1',
      [userId]
    );

    if (userResult.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }

    const user = userResult.rows[0];

    // Get active subscription
    const subscriptionResult = await db.query(
      'SELECT id, status, start_date, end_date FROM subscriptions WHERE user_id = $1 AND status = $2 ORDER BY created_at DESC LIMIT 1',
      [userId, 'active']
    );

    if (subscriptionResult.rows.length === 0) {
      return res.status(403).json({ error: 'No active subscription found' });
    }

    const subscription = subscriptionResult.rows[0];

    // Generate membership ID
    const membershipId = `AYUR${userId.substring(0, 8).toUpperCase()}`;

    // Return card data (frontend will generate PDF)
    res.status(200).json({
      success: true,
      cardData: {
        membershipId,
        name: user.name,
        email: user.email,
        role: user.role,
        profileImage: user.profile_image,
        startDate: subscription.start_date,
        endDate: subscription.end_date,
        status: subscription.status
      }
    });
  } catch (error) {
    console.error('Card generation error:', error);
    res.status(500).json({ error: 'Failed to generate membership card' });
  }
};

module.exports = authMiddleware(handler);
