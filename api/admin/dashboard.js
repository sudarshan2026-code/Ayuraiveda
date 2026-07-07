const { adminMiddleware } = require('../../middleware/auth');
const db = require('../../lib/db');

const handler = async (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Total users
    const totalUsersResult = await db.query(
      'SELECT COUNT(*) as count FROM users WHERE role != $1',
      ['admin']
    );
    const totalUsers = parseInt(totalUsersResult.rows[0].count);

    // Total revenue
    const revenueResult = await db.query(
      'SELECT COALESCE(SUM(amount), 0) as total FROM payments WHERE payment_status = $1',
      ['completed']
    );
    const totalRevenue = parseInt(revenueResult.rows[0].total);

    // Active subscriptions
    const activeSubsResult = await db.query(
      'SELECT COUNT(*) as count FROM subscriptions WHERE status = $1 AND end_date > NOW()',
      ['active']
    );
    const activeSubscriptions = parseInt(activeSubsResult.rows[0].count);

    // Recent users
    const recentUsersResult = await db.query(
      'SELECT id, name, email, role, created_at FROM users WHERE role != $1 ORDER BY created_at DESC LIMIT 10',
      ['admin']
    );

    // User breakdown by role
    const roleBreakdownResult = await db.query(
      'SELECT role, COUNT(*) as count FROM users WHERE role != $1 GROUP BY role',
      ['admin']
    );

    // Recent payments
    const recentPaymentsResult = await db.query(
      `SELECT p.id, p.amount, p.payment_status, p.created_at, u.name, u.email 
       FROM payments p 
       JOIN users u ON p.user_id = u.id 
       ORDER BY p.created_at DESC LIMIT 10`
    );

    res.status(200).json({
      success: true,
      stats: {
        totalUsers,
        totalRevenue,
        activeSubscriptions
      },
      recentUsers: recentUsersResult.rows,
      roleBreakdown: roleBreakdownResult.rows,
      recentPayments: recentPaymentsResult.rows
    });
  } catch (error) {
    console.error('Admin dashboard error:', error);
    res.status(500).json({ error: 'Failed to fetch dashboard data' });
  }
};

module.exports = adminMiddleware(handler);
