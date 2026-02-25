// Tridosha Intelligence Engine Security System

// Disable right-click
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    showSecurityPopup();
});

// Disable F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
document.addEventListener('keydown', function(e) {
    // F12
    if (e.keyCode === 123) {
        e.preventDefault();
        return false;
    }
    
    // Ctrl+Shift+I (Inspect)
    if (e.ctrlKey && e.shiftKey && e.keyCode === 73) {
        e.preventDefault();
        return false;
    }
    
    // Ctrl+Shift+J (Console)
    if (e.ctrlKey && e.shiftKey && e.keyCode === 74) {
        e.preventDefault();
        return false;
    }
    
    // Ctrl+U (View Source)
    if (e.ctrlKey && e.keyCode === 85) {
        e.preventDefault();
        return false;
    }
    
    // Ctrl+Shift+C (Inspect Element)
    if (e.ctrlKey && e.shiftKey && e.keyCode === 67) {
        e.preventDefault();
        return false;
    }
    
    // Ctrl+S (Save)
    if (e.ctrlKey && e.keyCode === 83) {
        e.preventDefault();
        return false;
    }
});

// Show security popup
function showSecurityPopup() {
    let overlay = document.getElementById('security-overlay');
    let popup = document.getElementById('security-popup');
    
    if (!overlay) {
        // Create overlay
        overlay = document.createElement('div');
        overlay.id = 'security-overlay';
        overlay.className = 'security-overlay';
        document.body.appendChild(overlay);
        
        // Create popup
        popup = document.createElement('div');
        popup.id = 'security-popup';
        popup.className = 'security-popup';
        popup.innerHTML = `
            <h3>🔒 Tridosha Intelligence Engine™</h3>
            <h4>Security System</h4>
            <p>This content is protected. Right-click is disabled for security purposes.</p>
            <button onclick="closeSecurityPopup()" class="btn" style="padding: 0.5rem 1.5rem; font-size: 0.9rem;">OK</button>
        `;
        document.body.appendChild(popup);
    }
    
    overlay.style.display = 'block';
    popup.style.display = 'block';
}

// Close security popup
function closeSecurityPopup() {
    document.getElementById('security-overlay').style.display = 'none';
    document.getElementById('security-popup').style.display = 'none';
}

// Close popup when clicking overlay
document.addEventListener('click', function(e) {
    if (e.target.id === 'security-overlay') {
        closeSecurityPopup();
    }
});
