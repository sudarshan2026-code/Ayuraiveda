const { adminMiddleware } = require('../../middleware/auth');
const db = require('../../lib/db');

const handler = async (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { page = 1, limit = 20, role, search } = req.query;
    const offset = (page - 1) * limit;

    let query = 'SELECT id, name, email, phone, role, profile_image, created_at FROM users WHERE role != $1';
    let countQuery = 'SELECT COUNT(*) as count FROM users WHERE role != $1';
    const params = ['admin'];
    let paramCount = 2;

    // Filter by role
    if (role && role !== 'all') {
      query += ` AND role = $${paramCount}`;
      countQuery += ` AND role = $${paramCount}`;
      params.push(role);
      paramCount++;
    }

    // Search by name or email
    if (search) {
      query += ` AND (name ILIKE $${paramCount} OR email ILIKE $${paramCount})`;
      countQuery += ` AND (name ILIKE $${paramCount} OR email ILIKE $${paramCount})`;
      params.push(`%${search}%`);
      paramCount++;
    }

    // Get total count
    const countResult = await db.query(countQuery, params);
    const totalUsers = parseInt(countResult.rows[0].count);

    // Get users with pagination
    query += ` ORDER BY created_at DESC LIMIT $${paramCount} OFFSET $${paramCount + 1}`;
    const usersResult = await db.query(query, [...params, limit, offset]);

    // Get subscription status for each user
    const usersWithSubscription = await Promise.all(
      usersResult.rows.map(async (user) => {
        const subResult = await db.query(
          'SELECT status, end_date FROM subscriptions WHERE user_id = $1 AND status = $2 ORDER BY created_at DESC LIMIT 1',
          [user.id, 'active']
        );
        return {
          ...user,
          subscription: subResult.rows[0] || null
        };
      })
    );

    res.status(200).json({
      success: true,
      users: usersWithSubscription,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total: totalUsers,
        totalPages: Math.ceil(totalUsers / limit)
      }
    });
  } catch (error) {
    console.error('Admin users list error:', error);
    res.status(500).json({ error: 'Failed to fetch users' });
  }
};

module.exports = adminMiddleware(handler);
