const { authMiddleware } = require('../../middleware/auth');
const db = require('../../lib/db');
const { sendReceiptEmail } = require('../../lib/email');

const handler = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const userId = req.user.id;
    const { orderId, cfPaymentId } = req.body;

    if (!orderId) {
      return res.status(400).json({ error: 'Order ID is required' });
    }

    // Get order
    const orderResult = await db.query(
      'SELECT id, amount FROM orders WHERE order_id = $1 AND user_id = $2',
      [orderId, userId]
    );

    if (orderResult.rows.length === 0) {
      return res.status(404).json({ error: 'Order not found' });
    }

    const order = orderResult.rows[0];

    // Update order status
    await db.query(
      'UPDATE orders SET status = $1 WHERE id = $2',
      ['completed', order.id]
    );

    // Update payment status
    await db.query(
      'UPDATE payments SET payment_status = $1, cf_payment_id = $2 WHERE order_id = $3',
      ['completed', cfPaymentId, order.id]
    );

    // Create or update subscription (30 days)
    const startDate = new Date();
    const endDate = new Date();
    endDate.setDate(endDate.getDate() + 30);

    await db.query(
      'INSERT INTO subscriptions (user_id, status, start_date, end_date) VALUES ($1, $2, $3, $4) ON CONFLICT (user_id) DO UPDATE SET status = $2, start_date = $3, end_date = $4',
      [userId, 'active', startDate, endDate]
    );

    // Get user details for email
    const userResult = await db.query(
      'SELECT name, email FROM users WHERE id = $1',
      [userId]
    );

    const user = userResult.rows[0];

    // Send receipt email
    await sendReceiptEmail(
      user.email,
      user.name,
      order.amount,
      orderId,
      startDate.toLocaleDateString('en-IN')
    );

    res.status(200).json({
      success: true,
      message: 'Payment confirmed and subscription activated',
      subscription: {
        status: 'active',
        startDate,
        endDate
      }
    });
  } catch (error) {
    console.error('Payment confirmation error:', error);
    res.status(500).json({ error: 'Failed to confirm payment' });
  }
};

module.exports = authMiddleware(handler);
