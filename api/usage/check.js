const { authMiddleware } = require('../../middleware/auth');
const db = require('../../lib/db');

const handler = async (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const userId = req.user.id;

    const subscriptionResult = await db.query(
      'SELECT status, end_date FROM subscriptions WHERE user_id = $1 AND status = $2 AND end_date > NOW() ORDER BY created_at DESC LIMIT 1',
      [userId, 'active']
    );

    const hasActiveSubscription = subscriptionResult.rows.length > 0;

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const assessmentResult = await db.query(
      'SELECT COUNT(*) as count FROM reports WHERE user_id = $1 AND created_at >= $2',
      [userId, today]
    );
    const assessmentsToday = parseInt(assessmentResult.rows[0].count);

    const chatMessagesToday = 0;

    const FREE_ASSESSMENT_LIMIT = 1;
    const FREE_CHAT_LIMIT = 10;

    const assessmentsRemaining = hasActiveSubscription 
      ? 'unlimited' 
      : Math.max(0, FREE_ASSESSMENT_LIMIT - assessmentsToday);

    const chatRemaining = hasActiveSubscription 
      ? 'unlimited' 
      : Math.max(0, FREE_CHAT_LIMIT - chatMessagesToday);

    res.status(200).json({
      success: true,
      subscription: {
        active: hasActiveSubscription,
        endDate: hasActiveSubscription ? subscriptionResult.rows[0].end_date : null
      },
      usage: {
        assessments: {
          used: assessmentsToday,
          remaining: assessmentsRemaining,
          limit: hasActiveSubscription ? 'unlimited' : FREE_ASSESSMENT_LIMIT
        },
        chat: {
          used: chatMessagesToday,
          remaining: chatRemaining,
          limit: hasActiveSubscription ? 'unlimited' : FREE_CHAT_LIMIT
        }
      }
    });
  } catch (error) {
    console.error('Usage check error:', error);
    res.status(500).json({ error: 'Failed to check usage' });
  }
};

module.exports = authMiddleware(handler);
