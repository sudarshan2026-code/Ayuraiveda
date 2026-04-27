/**
 * Clinical Report Generator - Frontend
 * Handles comprehensive Ayurvedic clinical report generation
 */

async function generateClinicalReport(userData, assessmentResults) {
    try {
        showLoadingIndicator('Generating comprehensive clinical report...');
        
        const response = await fetch('/generate-clinical-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_data: userData,
                assessment_results: assessmentResults
            })
        });
        
        const data = await response.json();
        
        hideLoadingIndicator();
        
        if (data.success) {
            displayClinicalReport(data.report);
            return data.report;
        } else {
            throw new Error(data.error || 'Failed to generate report');
        }
    } catch (error) {
        hideLoadingIndicator();
        console.error('Report generation error:', error);
        alert('Failed to generate clinical report. Please try again.');
        return null;
    }
}

function displayClinicalReport(report) {
    const reportContainer = document.getElementById('clinical-report-container');
    if (!reportContainer) {
        console.error('Report container not found');
        return;
    }
    
    let html = `
        <div class="clinical-report">
            <div class="report-header">
                <h2>🕉️ Ayurvedic Clinical Assessment Report</h2>
                <p class="report-subtitle">Powered by Tridosha Intelligence Engine™</p>
            </div>
            
            <!-- Personal Details -->
            <div class="report-section">
                <h3>👤 Personal Details</h3>
                <div class="info-grid">
                    <div class="info-item">
                        <span class="info-label">Name:</span>
                        <span class="info-value">${report.personal_details.name}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Age:</span>
                        <span class="info-value">${report.personal_details.age}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Gender:</span>
                        <span class="info-value">${report.personal_details.gender}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Location:</span>
                        <span class="info-value">${report.personal_details.location}</span>
                    </div>
                </div>
            </div>
            
            <!-- Dosha Analysis -->
            <div class="report-section">
                <h3>🧠 Dosha Analysis</h3>
                <div class="dosha-analysis">
                    <div class="analysis-item">
                        <strong>Dominant Dosha:</strong> ${report.dosha_analysis.dominant_dosha}
                    </div>
                    <div class="analysis-item">
                        <strong>Secondary Dosha:</strong> ${report.dosha_analysis.secondary_dosha}
                    </div>
                    <div class="analysis-item">
                        <strong>Current Imbalance (Vikriti):</strong> ${report.dosha_analysis.vikriti}
                    </div>
                    <div class="analysis-explanation">
                        <p>${report.dosha_analysis.explanation}</p>
                    </div>
                </div>
            </div>
            
            <!-- Diet Recommendations -->
            <div class="report-section">
                <h3>🥗 Diet Recommendations</h3>
                
                <div class="diet-subsection">
                    <h4>✅ Foods to Take:</h4>
                    <ul class="recommendation-list">
                        ${report.diet_recommendations.foods_to_take.map(food => `<li>${food}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="diet-subsection">
                    <h4>❌ Foods to Avoid:</h4>
                    <ul class="recommendation-list avoid-list">
                        ${report.diet_recommendations.foods_to_avoid.map(food => `<li>${food}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="diet-subsection">
                    <h4>💡 Eating Guidelines:</h4>
                    <ul class="recommendation-list">
                        ${report.diet_recommendations.eating_guidelines.map(guideline => `<li>${guideline}</li>`).join('')}
                    </ul>
                </div>
            </div>
            
            <!-- Lifestyle Recommendations -->
            <div class="report-section">
                <h3>🧘 Lifestyle Recommendations</h3>
                
                <div class="lifestyle-subsection">
                    <h4>🌿 Daily Routine (Dinacharya):</h4>
                    <ul class="recommendation-list">
                        ${report.lifestyle_recommendations.daily_routine.map(routine => `<li>${routine}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="lifestyle-subsection">
                    <h4>🧘‍♂️ Yoga Practices:</h4>
                    <ul class="recommendation-list">
                        ${report.lifestyle_recommendations.practices.yoga.map(yoga => `<li>${yoga}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="lifestyle-subsection">
                    <h4>🌬️ Pranayama:</h4>
                    <ul class="recommendation-list">
                        ${report.lifestyle_recommendations.practices.pranayama.map(prana => `<li>${prana}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="lifestyle-subsection">
                    <h4>🧘 Meditation:</h4>
                    <ul class="recommendation-list">
                        ${report.lifestyle_recommendations.practices.meditation.map(med => `<li>${med}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="lifestyle-subsection">
                    <h4>⚠️ Habits to Avoid:</h4>
                    <ul class="recommendation-list avoid-list">
                        ${report.lifestyle_recommendations.habits_to_avoid.map(habit => `<li>${habit}</li>`).join('')}
                    </ul>
                </div>
            </div>
            
            <!-- Herbal Support -->
            <div class="report-section">
                <h3>🌱 Herbal Support</h3>
                
                <div class="herbal-subsection">
                    <h4>🌿 Recommended Herbs:</h4>
                    <ul class="recommendation-list">
                        ${report.herbal_support.recommended_herbs.map(herb => `<li>${herb}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="herbal-subsection">
                    <h4>💊 Usage Guidance:</h4>
                    <ul class="recommendation-list">
                        ${report.herbal_support.usage_guidance.map(usage => `<li>${usage}</li>`).join('')}
                    </ul>
                </div>
                
                ${report.herbal_support.avoid && report.herbal_support.avoid.length > 0 ? `
                <div class="herbal-subsection">
                    <h4>⚠️ Avoid:</h4>
                    <ul class="recommendation-list avoid-list">
                        ${report.herbal_support.avoid.map(avoid => `<li>${avoid}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
            </div>
            
            <!-- Additional Wellness Advice -->
            <div class="report-section">
                <h3>🧭 Additional Wellness Advice</h3>
                
                <div class="wellness-subsection">
                    <h4>🌸 Seasonal Care (Ritucharya):</h4>
                    <ul class="recommendation-list">
                        ${report.wellness_advice.seasonal_tips.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="wellness-subsection">
                    <h4>😌 Stress Management:</h4>
                    <ul class="recommendation-list">
                        ${report.wellness_advice.stress_management.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="wellness-subsection">
                    <h4>🔥 Digestive Care:</h4>
                    <ul class="recommendation-list">
                        ${report.wellness_advice.digestive_care.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
            </div>
            
            <!-- Disclaimer -->
            <div class="report-disclaimer">
                <p><strong>⚠️ Important Disclaimer:</strong> ${report.disclaimer}</p>
            </div>
            
            <!-- Action Buttons -->
            <div class="report-actions">
                <button class="btn btn-primary" onclick="downloadClinicalReportPDF()">
                    📥 Download PDF Report
                </button>
                <button class="btn btn-secondary" onclick="printClinicalReport()">
                    🖨️ Print Report
                </button>
                <button class="btn btn-secondary" onclick="emailClinicalReport()">
                    📧 Email Report
                </button>
            </div>
            
            <div class="report-footer">
                <p>🌿 <strong>AyurAI Veda</strong> | Ancient Wisdom. Intelligent Health.</p>
                <p>Powered by Tridosha Intelligence Engine™</p>
                <p class="timestamp">Report generated on ${report.timestamp}</p>
            </div>
        </div>
    `;
    
    reportContainer.innerHTML = html;
    reportContainer.style.display = 'block';
    
    // Scroll to report
    reportContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function downloadClinicalReportPDF() {
    try {
        showLoadingIndicator('Generating PDF...');
        
        // Get the current report data
        const reportData = getCurrentReportData();
        
        const response = await fetch('/download-clinical-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ report: reportData })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate PDF');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `AyurAI_Clinical_Report_${new Date().getTime()}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        hideLoadingIndicator();
        alert('✅ PDF report downloaded successfully!');
    } catch (error) {
        hideLoadingIndicator();
        console.error('PDF download error:', error);
        alert('Failed to download PDF. Please try again.');
    }
}

function printClinicalReport() {
    window.print();
}

async function emailClinicalReport() {
    const email = prompt('Enter your email address:');
    if (!email) return;
    
    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Please enter a valid email address');
        return;
    }
    
    try {
        showLoadingIndicator('Sending report to your email...');
        
        const reportData = getCurrentReportData();
        
        const response = await fetch('/send-report-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                report_data: reportData
            })
        });
        
        const data = await response.json();
        
        hideLoadingIndicator();
        
        if (data.success) {
            alert(`✅ Report sent successfully to ${email}`);
        } else {
            alert('Failed to send email. Please try again.');
        }
    } catch (error) {
        hideLoadingIndicator();
        console.error('Email error:', error);
        alert('Failed to send email. Please try again.');
    }
}

function getCurrentReportData() {
    // This should be stored globally when report is generated
    return window.currentClinicalReport || {};
}

function showLoadingIndicator(message = 'Loading...') {
    let loader = document.getElementById('loading-indicator');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'loading-indicator';
        loader.className = 'loading-overlay';
        loader.innerHTML = `
            <div class="loading-content">
                <div class="spinner"></div>
                <p>${message}</p>
            </div>
        `;
        document.body.appendChild(loader);
    } else {
        loader.querySelector('p').textContent = message;
    }
    loader.style.display = 'flex';
}

function hideLoadingIndicator() {
    const loader = document.getElementById('loading-indicator');
    if (loader) {
        loader.style.display = 'none';
    }
}

// Add CSS for clinical report
const reportStyles = `
<style>
.clinical-report {
    max-width: 900px;
    margin: 2rem auto;
    padding: 2rem;
    background: var(--card-bg);
    border-radius: 8px;
    box-shadow: 0 5px 20px var(--shadow);
}

.report-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 3px solid var(--primary);
}

.report-header h2 {
    color: var(--primary);
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.report-subtitle {
    color: var(--light-text);
    font-size: 1rem;
    opacity: 0.9;
}

.report-section {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: var(--darker);
    border-radius: 6px;
    border-left: 4px solid var(--primary);
}

.report-section h3 {
    color: var(--primary);
    font-size: 1.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--secondary);
}

.report-section h4 {
    color: var(--secondary);
    font-size: 1.2rem;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.info-label {
    font-weight: 600;
    color: var(--primary);
    font-size: 0.9rem;
}

.info-value {
    color: var(--light-text);
    font-size: 1rem;
}

.dosha-analysis {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.analysis-item {
    padding: 0.75rem;
    background: var(--card-bg);
    border-radius: 4px;
    color: var(--light-text);
}

.analysis-explanation {
    padding: 1rem;
    background: var(--card-bg);
    border-radius: 4px;
    border-left: 3px solid var(--accent);
    margin-top: 0.5rem;
}

.analysis-explanation p {
    color: var(--light-text);
    line-height: 1.6;
}

.diet-subsection,
.lifestyle-subsection,
.herbal-subsection,
.wellness-subsection {
    margin-bottom: 1.5rem;
}

.recommendation-list {
    list-style: none;
    padding-left: 0;
    margin-top: 0.5rem;
}

.recommendation-list li {
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background: var(--card-bg);
    border-left: 3px solid var(--primary);
    border-radius: 4px;
    color: var(--light-text);
    line-height: 1.5;
}

.recommendation-list.avoid-list li {
    border-left-color: var(--accent);
    background: rgba(255, 46, 151, 0.1);
}

.report-disclaimer {
    padding: 1rem;
    background: rgba(255, 46, 151, 0.1);
    border: 1px solid var(--accent);
    border-radius: 6px;
    margin: 2rem 0;
}

.report-disclaimer p {
    color: var(--light-text);
    font-size: 0.9rem;
    margin: 0;
}

.report-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 2rem 0;
}

.report-footer {
    text-align: center;
    padding-top: 2rem;
    border-top: 2px solid var(--border);
    color: var(--light-text);
}

.report-footer p {
    margin: 0.5rem 0;
}

.timestamp {
    font-size: 0.85rem;
    opacity: 0.7;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(10, 14, 39, 0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
}

.loading-content {
    text-align: center;
    color: var(--light-text);
}

.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid var(--border);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

@media print {
    .report-actions,
    .loading-overlay {
        display: none !important;
    }
    
    .clinical-report {
        box-shadow: none;
        padding: 1rem;
    }
}

@media (max-width: 768px) {
    .clinical-report {
        padding: 1rem;
    }
    
    .report-header h2 {
        font-size: 1.5rem;
    }
    
    .report-section {
        padding: 1rem;
    }
    
    .report-section h3 {
        font-size: 1.3rem;
    }
    
    .report-actions {
        flex-direction: column;
    }
    
    .report-actions .btn {
        width: 100%;
    }
}
</style>
`;

// Inject styles
if (!document.getElementById('clinical-report-styles')) {
    const styleElement = document.createElement('div');
    styleElement.id = 'clinical-report-styles';
    styleElement.innerHTML = reportStyles;
    document.head.appendChild(styleElement);
}
