const { authMiddleware } = require('../../middleware/auth');
const db = require('../../lib/db');

const handler = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const userId = req.user.id;
    const { role } = req.user;

    // Only users can purchase membership
    if (role !== 'user') {
      return res.status(403).json({ error: 'Only users can purchase membership' });
    }

    const { amount } = req.body;

    if (!amount || amount <= 0) {
      return res.status(400).json({ error: 'Invalid amount' });
    }

    // Create order
    const orderId = `ORDER_${Date.now()}_${userId.substring(0, 8)}`;
    
    const orderResult = await db.query(
      'INSERT INTO orders (user_id, order_id, amount, status) VALUES ($1, $2, $3, $4) RETURNING id, order_id',
      [userId, orderId, amount, 'pending']
    );

    const order = orderResult.rows[0];

    // Create payment record
    await db.query(
      'INSERT INTO payments (user_id, order_id, amount, payment_status) VALUES ($1, $2, $3, $4)',
      [userId, order.id, amount, 'pending']
    );

    // Return Cashfree payment link
    res.status(200).json({
      success: true,
      orderId: order.order_id,
      paymentLink: process.env.CASHFREE_PAYMENT_LINK,
      amount
    });
  } catch (error) {
    console.error('Payment initiation error:', error);
    res.status(500).json({ error: 'Failed to initiate payment' });
  }
};

module.exports = authMiddleware(handler);
