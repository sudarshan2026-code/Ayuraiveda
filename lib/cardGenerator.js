import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export const generateMembershipCard = async (cardData) => {
  const {
    membershipId,
    name,
    email,
    role,
    profileImage,
    startDate,
    endDate
  } = cardData;

  // Create card HTML
  const cardHTML = `
    <div id="membership-card" style="
      width: 800px;
      height: 500px;
      background: linear-gradient(135deg, #2A9D8F 0%, #264653 100%);
      border-radius: 20px;
      padding: 30px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      font-family: Arial, sans-serif;
      color: white;
      position: relative;
    ">
      <!-- MSME Badge -->
      <div style="
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(255,255,255,0.2);
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
      ">
        MSME Registered | UDYAM-GJ-24-0218250
      </div>

      <!-- Header -->
      <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="margin: 0; font-size: 36px; font-weight: bold;">🕉️ AyurAI Veda</h1>
        <p style="margin: 5px 0; font-size: 14px; opacity: 0.9;">Ananta Labs India</p>
        <p style="margin: 0; font-size: 12px; opacity: 0.8;">Powered by Tridosha Intelligence Engine™</p>
      </div>

      <!-- Card Content -->
      <div style="display: flex; gap: 30px; align-items: center;">
        <!-- Profile Image -->
        <div style="flex-shrink: 0;">
          <div style="
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border: 5px solid rgba(255,255,255,0.3);
          ">
            ${profileImage 
              ? `<img src="${profileImage}" style="width: 100%; height: 100%; object-fit: cover;" />`
              : `<div style="font-size: 60px; color: #2A9D8F;">👤</div>`
            }
          </div>
        </div>

        <!-- Details -->
        <div style="flex: 1;">
          <div style="margin-bottom: 15px;">
            <div style="font-size: 12px; opacity: 0.8; margin-bottom: 3px;">Member Name</div>
            <div style="font-size: 24px; font-weight: bold;">${name}</div>
          </div>

          <div style="margin-bottom: 15px;">
            <div style="font-size: 12px; opacity: 0.8; margin-bottom: 3px;">Email</div>
            <div style="font-size: 16px;">${email}</div>
          </div>

          <div style="display: flex; gap: 30px; margin-bottom: 15px;">
            <div>
              <div style="font-size: 12px; opacity: 0.8; margin-bottom: 3px;">Role</div>
              <div style="font-size: 16px; font-weight: bold; text-transform: uppercase;">${role}</div>
            </div>
            <div>
              <div style="font-size: 12px; opacity: 0.8; margin-bottom: 3px;">Membership ID</div>
              <div style="font-size: 16px; font-weight: bold;">${membershipId}</div>
            </div>
          </div>

          <div style="display: flex; gap: 30px;">
            <div>
              <div style="font-size: 12px; opacity: 0.8; margin-bottom: 3px;">Start Date</div>
              <div style="font-size: 14px;">${new Date(startDate).toLocaleDateString('en-IN')}</div>
            </div>
            <div>
              <div style="font-size: 12px; opacity: 0.8; margin-bottom: 3px;">Expiry Date</div>
              <div style="font-size: 14px;">${new Date(endDate).toLocaleDateString('en-IN')}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div style="
        position: absolute;
        bottom: 20px;
        left: 30px;
        right: 30px;
        text-align: center;
        font-size: 11px;
        opacity: 0.7;
        border-top: 1px solid rgba(255,255,255,0.3);
        padding-top: 15px;
      ">
        This card is valid for premium access to AyurAI Veda services
      </div>
    </div>
  `;

  // Create temporary container
  const container = document.createElement('div');
  container.innerHTML = cardHTML;
  container.style.position = 'absolute';
  container.style.left = '-9999px';
  document.body.appendChild(container);

  try {
    // Convert to canvas
    const canvas = await html2canvas(container.firstElementChild, {
      scale: 2,
      backgroundColor: null
    });

    // Create PDF
    const pdf = new jsPDF({
      orientation: 'landscape',
      unit: 'px',
      format: [800, 500]
    });

    const imgData = canvas.toDataURL('image/png');
    pdf.addImage(imgData, 'PNG', 0, 0, 800, 500);

    // Download
    pdf.save(`AyurAI_Veda_Membership_${membershipId}.pdf`);

    return { success: true };
  } catch (error) {
    console.error('Card generation error:', error);
    return { success: false, error: error.message };
  } finally {
    // Cleanup
    document.body.removeChild(container);
  }
};
