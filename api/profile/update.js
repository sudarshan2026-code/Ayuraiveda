const { authMiddleware } = require('../../middleware/auth');
const db = require('../../lib/db');

const handler = async (req, res) => {
  if (req.method !== 'PUT') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const userId = req.user.id;
    const { role } = req.user;
    const data = req.body;

    // Update user basic info if provided
    if (data.name || data.phone || data.profile_image) {
      const updates = [];
      const values = [];
      let paramCount = 1;

      if (data.name) {
        updates.push(`name = $${paramCount++}`);
        values.push(data.name);
      }
      if (data.phone) {
        updates.push(`phone = $${paramCount++}`);
        values.push(data.phone);
      }
      if (data.profile_image) {
        updates.push(`profile_image = $${paramCount++}`);
        values.push(data.profile_image);
      }

      values.push(userId);

      await db.query(
        `UPDATE users SET ${updates.join(', ')} WHERE id = $${paramCount}`,
        values
      );
    }

    // Update role-specific profile
    if (role === 'user') {
      const { age, gender, additional_details } = data;
      await db.query(
        'UPDATE user_profiles SET age = COALESCE($1, age), gender = COALESCE($2, gender), additional_details = COALESCE($3, additional_details) WHERE user_id = $4',
        [age, gender, additional_details, userId]
      );
    } else if (role === 'doctor') {
      const { specialization, experience, clinic_name, additional_details } = data;
      await db.query(
        'UPDATE doctor_profiles SET specialization = COALESCE($1, specialization), experience = COALESCE($2, experience), clinic_name = COALESCE($3, clinic_name), additional_details = COALESCE($4, additional_details) WHERE user_id = $5',
        [specialization, experience, clinic_name, additional_details, userId]
      );
    } else if (role === 'college') {
      const { college_name, course, year, additional_details } = data;
      await db.query(
        'UPDATE college_profiles SET college_name = COALESCE($1, college_name), course = COALESCE($2, course), year = COALESCE($3, year), additional_details = COALESCE($4, additional_details) WHERE user_id = $5',
        [college_name, course, year, additional_details, userId]
      );
    }

    res.status(200).json({
      success: true,
      message: 'Profile updated successfully'
    });
  } catch (error) {
    console.error('Profile update error:', error);
    res.status(500).json({ error: 'Failed to update profile' });
  }
};

module.exports = authMiddleware(handler);
