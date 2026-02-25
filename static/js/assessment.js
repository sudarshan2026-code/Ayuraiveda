let currentResults = null;

document.getElementById('healthForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    // Show thinking indicator
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '🧠 Analyzing with Tridosha Intelligence Engine<span class="dots">...</span>';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        currentResults = result;
        displayResults(result);
    } catch (error) {
        alert('Error analyzing data. Please try again.');
        console.error(error);
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

function displayResults(result) {
    document.getElementById('assessment-form').style.display = 'none';
    document.getElementById('results').style.display = 'block';
    
    document.getElementById('dominant').textContent = result.dominant;
    document.getElementById('description').textContent = result.description;
    
    const riskBadge = document.getElementById('risk-badge');
    riskBadge.textContent = `Risk Level: ${result.risk}`;
    riskBadge.className = 'risk-badge risk-' + result.risk.toLowerCase();
    
    setTimeout(() => {
        document.getElementById('vata-fill').style.width = result.scores.vata + '%';
        document.getElementById('vata-fill').textContent = result.scores.vata + '%';
        
        document.getElementById('pitta-fill').style.width = result.scores.pitta + '%';
        document.getElementById('pitta-fill').textContent = result.scores.pitta + '%';
        
        document.getElementById('kapha-fill').style.width = result.scores.kapha + '%';
        document.getElementById('kapha-fill').textContent = result.scores.kapha + '%';
    }, 100);
    
    // Display disease predictions
    if (result.disease_prediction) {
        const diseaseSection = document.getElementById('disease-predictions');
        if (diseaseSection) {
            diseaseSection.style.display = 'block';
            
            const diseaseList = document.getElementById('disease-list');
            diseaseList.innerHTML = '';
            result.disease_prediction.diseases.forEach(disease => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${disease}</strong>`;
                if (disease === result.disease_prediction.primary_risk) {
                    li.innerHTML += ' <span class="primary-risk">⚠️ Primary Risk</span>';
                }
                diseaseList.appendChild(li);
            });
            
            const riskList = document.getElementById('risk-factors-list');
            riskList.innerHTML = '';
            result.disease_prediction.risk_factors.forEach(risk => {
                const li = document.createElement('li');
                li.textContent = risk;
                riskList.appendChild(li);
            });
        }
    }
    
    const recList = document.getElementById('recommendations-list');
    recList.innerHTML = '';
    result.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recList.appendChild(li);
    });
    
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

async function downloadReport() {
    if (!currentResults) return;
    
    const language = document.getElementById('language-selector').value;
    const reportData = {
        ...currentResults,
        language: language
    };
    
    try {
        const response = await fetch('/download-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reportData)
        });
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `AyurAI_Veda_Report_${language}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        alert('Error downloading report. Please try again.');
        console.error(error);
    }
}
