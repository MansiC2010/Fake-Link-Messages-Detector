// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        
        // Update buttons
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update content
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.getElementById(`${tab}-tab`).classList.add('active');
        
        // Clear results
        clearResults();
    });
});

// Clear results
function clearResults() {
    document.getElementById('url-result').classList.remove('show');
    document.getElementById('message-result').classList.remove('show');
    document.getElementById('url-result').innerHTML = '';
    document.getElementById('message-result').innerHTML = '';
}

// URL Detection
document.getElementById('detect-url-btn').addEventListener('click', () => {
    const url = document.getElementById('url-input').value.trim();
    
    if (!url) {
        showError('url-result', 'Please enter a URL');
        return;
    }
    
    detectURL(url);
});

// Enter key for URL
document.getElementById('url-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        document.getElementById('detect-url-btn').click();
    }
});

// Message Detection
document.getElementById('detect-message-btn').addEventListener('click', () => {
    const message = document.getElementById('message-input').value.trim();
    
    if (!message) {
        showError('message-result', 'Please enter a message');
        return;
    }
    
    detectMessage(message);
});

// Detect URL
async function detectURL(url) {
    const resultContainer = document.getElementById('url-result');
    resultContainer.classList.add('show');
    resultContainer.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i><p>Analyzing URL with AI...</p></div>';
    
    const btn = document.getElementById('detect-url-btn');
    btn.disabled = true;
    
    try {
        const response = await fetch('/detect/url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResult('url-result', data, 'url');
        } else {
            showError('url-result', data.error || 'Detection failed');
        }
    } catch (error) {
        showError('url-result', 'Network error. Please try again.');
    } finally {
        btn.disabled = false;
    }
}

// Detect Message
async function detectMessage(message) {
    const resultContainer = document.getElementById('message-result');
    resultContainer.classList.add('show');
    resultContainer.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i><p>Analyzing message with AI...</p></div>';
    
    const btn = document.getElementById('detect-message-btn');
    btn.disabled = true;
    
    try {
        const response = await fetch('/detect/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResult('message-result', data, 'message');
        } else {
            showError('message-result', data.error || 'Detection failed');
        }
    } catch (error) {
        showError('message-result', 'Network error. Please try again.');
    } finally {
        btn.disabled = false;
    }
}

// Display Result
function displayResult(containerId, data, type) {
    const container = document.getElementById(containerId);
    const isFake = data.is_fake;
    const status = isFake ? 'FAKE' : 'LEGITIMATE';
    const statusClass = isFake ? 'fake' : 'legitimate';
    const icon = isFake ? 'fa-exclamation-triangle' : 'fa-check-circle';
    
    let reasonsHTML = '';
    if (data.reasons && data.reasons.length > 0) {
        reasonsHTML = '<ul class="reasons-list">';
        data.reasons.forEach(reason => {
            const isWarning = reason.includes('[WARNING]');
            const isOk = reason.includes('[OK]');
            const reasonClass = isWarning ? 'warning' : (isOk ? 'ok' : '');
            const reasonIcon = isWarning ? 'fa-exclamation-circle' : (isOk ? 'fa-check' : 'fa-info-circle');
            const cleanReason = reason.replace(/\[WARNING\]|\[OK\]/g, '').trim();
            
            reasonsHTML += `
                <li class="reason-item ${reasonClass}">
                    <i class="fas ${reasonIcon}"></i>
                    <span>${cleanReason}</span>
                </li>
            `;
        });
        reasonsHTML += '</ul>';
    }
    
    container.innerHTML = `
        <div class="result-card">
            <div class="result-header">
                <div class="result-status ${statusClass}">
                    <i class="fas ${icon}"></i>
                    <span>${status}</span>
                </div>
                <div class="confidence-badge ${statusClass}">
                    ${data.confidence}% Confidence
                </div>
            </div>
            ${type === 'url' ? `<p style="color: var(--text-secondary); margin-bottom: 20px; word-break: break-all;">${data.url}</p>` : ''}
            ${reasonsHTML}
        </div>
    `;

}

// Show Error
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-circle"></i> ${message}
        </div>
    `;
}

// Analytics
const generateChartBtn = document.getElementById('generate-chart-btn');
if (generateChartBtn) {
    generateChartBtn.addEventListener('click', async () => {
        const dataset = document.getElementById('dataset-select').value;
        const chart = document.getElementById('chart-select').value;
        const chartArea = document.getElementById('chart-area');

        chartArea.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i><p>Generating chart...</p></div>';

        try {
            const response = await fetch('/analytics', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filter_type: dataset, chart_type: chart })
            });
            const data = await response.json();
            if (!data.success) {
                chartArea.innerHTML = `<p class="chart-placeholder">${data.error || 'Unable to generate chart.'}</p>`;
                return;
            }

            chartArea.innerHTML = `<img src="data:image/png;base64,${data.image}" alt="Analytics chart" />`;
        } catch (err) {
            chartArea.innerHTML = '<p class="chart-placeholder">Error generating chart.</p>';
        }
    });
}



