/**
 * AyurAI Veda - Security System
 * Protects content from unauthorized copying and inspection
 */

(function() {
    'use strict';

    // ============= RIGHT-CLICK PROTECTION =============
    
    // Disable right-click context menu
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        showSecurityAlert('Right-click is disabled to protect content');
        return false;
    });

    // ============= KEYBOARD SHORTCUTS PROTECTION =============
    
    document.addEventListener('keydown', function(e) {
        // Disable F12 (Developer Tools)
        if (e.keyCode === 123) {
            e.preventDefault();
            showSecurityAlert('Developer tools are disabled');
            return false;
        }
        
        // Disable Ctrl+Shift+I (Inspect Element)
        if (e.ctrlKey && e.shiftKey && e.keyCode === 73) {
            e.preventDefault();
            showSecurityAlert('Inspect element is disabled');
            return false;
        }
        
        // Disable Ctrl+Shift+J (Console)
        if (e.ctrlKey && e.shiftKey && e.keyCode === 74) {
            e.preventDefault();
            showSecurityAlert('Console is disabled');
            return false;
        }
        
        // Disable Ctrl+Shift+C (Inspect Element)
        if (e.ctrlKey && e.shiftKey && e.keyCode === 67) {
            e.preventDefault();
            showSecurityAlert('Inspect element is disabled');
            return false;
        }
        
        // Disable Ctrl+U (View Source)
        if (e.ctrlKey && e.keyCode === 85) {
            e.preventDefault();
            showSecurityAlert('View source is disabled');
            return false;
        }
        
        // Disable Ctrl+S (Save Page)
        if (e.ctrlKey && e.keyCode === 83) {
            e.preventDefault();
            showSecurityAlert('Saving page is disabled');
            return false;
        }
        
        // Disable Ctrl+P (Print)
        if (e.ctrlKey && e.keyCode === 80) {
            e.preventDefault();
            showSecurityAlert('Printing is disabled');
            return false;
        }
        
        // Disable Ctrl+A (Select All) - Optional
        // Uncomment if you want to disable text selection
        /*
        if (e.ctrlKey && e.keyCode === 65) {
            e.preventDefault();
            showSecurityAlert('Select all is disabled');
            return false;
        }
        */
        
        // Disable Ctrl+C (Copy) - Optional
        // Uncomment if you want to disable copying
        /*
        if (e.ctrlKey && e.keyCode === 67) {
            e.preventDefault();
            showSecurityAlert('Copying is disabled');
            return false;
        }
        */
    });

    // ============= TEXT SELECTION PROTECTION =============
    
    // Disable text selection (optional - uncomment to enable)
    /*
    document.addEventListener('selectstart', function(e) {
        e.preventDefault();
        return false;
    });
    
    document.addEventListener('mousedown', function(e) {
        if (e.detail > 1) {
            e.preventDefault();
            return false;
        }
    });
    */

    // ============= COPY/CUT/PASTE PROTECTION =============
    
    // Disable copy (optional - uncomment to enable)
    /*
    document.addEventListener('copy', function(e) {
        e.preventDefault();
        showSecurityAlert('Copying is disabled');
        return false;
    });
    */
    
    // Disable cut (optional - uncomment to enable)
    /*
    document.addEventListener('cut', function(e) {
        e.preventDefault();
        showSecurityAlert('Cutting is disabled');
        return false;
    });
    */

    // ============= DRAG AND DROP PROTECTION =============
    
    document.addEventListener('dragstart', function(e) {
        e.preventDefault();
        return false;
    });

    // ============= DEVELOPER TOOLS DETECTION =============
    
    // Detect if developer tools are open
    let devtoolsOpen = false;
    const element = new Image();
    
    Object.defineProperty(element, 'id', {
        get: function() {
            devtoolsOpen = true;
            showSecurityAlert('Developer tools detected');
        }
    });
    
    setInterval(function() {
        devtoolsOpen = false;
        console.log(element);
        console.clear();
    }, 1000);

    // ============= CONSOLE PROTECTION =============
    
    // Disable console methods
    if (!window.console) window.console = {};
    const methods = ['log', 'debug', 'warn', 'info', 'error', 'dir', 'trace'];
    
    for (let i = 0; i < methods.length; i++) {
        console[methods[i]] = function() {};
    }

    // ============= SECURITY ALERT FUNCTION =============
    
    function showSecurityAlert(message) {
        // Create custom alert overlay
        const alertDiv = document.createElement('div');
        alertDiv.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #FF9933, #138808);
            color: white;
            padding: 20px 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            z-index: 999999;
            font-family: Arial, sans-serif;
            text-align: center;
            animation: slideIn 0.3s ease-out;
        `;
        
        alertDiv.innerHTML = `
            <div style="font-size: 40px; margin-bottom: 10px;">🔒</div>
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">Content Protected</div>
            <div style="font-size: 14px; opacity: 0.9;">${message}</div>
            <div style="font-size: 12px; margin-top: 15px; opacity: 0.7;">AyurAI Veda™ - All Rights Reserved</div>
        `;
        
        // Add animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translate(-50%, -60%);
                }
                to {
                    opacity: 1;
                    transform: translate(-50%, -50%);
                }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(alertDiv);
        
        // Remove alert after 2 seconds
        setTimeout(function() {
            alertDiv.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(function() {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 300);
        }, 2000);
    }

    // ============= WATERMARK PROTECTION =============
    
    // Add invisible watermark to page
    function addWatermark() {
        const watermark = document.createElement('div');
        watermark.style.cssText = `
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 10px;
            color: rgba(0,0,0,0.1);
            pointer-events: none;
            z-index: 999998;
            user-select: none;
        `;
        watermark.textContent = 'AyurAI Veda™ © ' + new Date().getFullYear();
        document.body.appendChild(watermark);
    }
    
    // Add watermark when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addWatermark);
    } else {
        addWatermark();
    }

    // ============= IFRAME PROTECTION =============
    
    // Prevent page from being loaded in iframe
    if (window.top !== window.self) {
        window.top.location = window.self.location;
    }

    // ============= SCREENSHOT PROTECTION =============
    
    // Add CSS to prevent screenshots (limited effectiveness)
    const style = document.createElement('style');
    style.textContent = `
        * {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        input, textarea {
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
        }
        
        img {
            pointer-events: none;
            -webkit-user-drag: none;
            -khtml-user-drag: none;
            -moz-user-drag: none;
            -o-user-drag: none;
            user-drag: none;
        }
    `;
    document.head.appendChild(style);

    // ============= PRINT PROTECTION =============
    
    window.addEventListener('beforeprint', function(e) {
        showSecurityAlert('Printing is disabled for security reasons');
        e.preventDefault();
        return false;
    });

    // ============= SECURITY LOGGING =============
    
    // Log security events (for debugging - remove in production)
    function logSecurityEvent(event) {
        // Send to analytics or logging service
        // console.log('Security Event:', event);
    }

    // ============= INITIALIZATION MESSAGE =============
    
    console.log('%c🔒 AyurAI Veda™ Security System Active', 
        'color: #FF9933; font-size: 16px; font-weight: bold;');
    console.log('%c⚠️ Unauthorized access or copying is prohibited', 
        'color: #d32f2f; font-size: 12px;');
    console.log('%c© ' + new Date().getFullYear() + ' AyurAI Veda. All Rights Reserved.', 
        'color: #666; font-size: 10px;');

})();

// ============= ADDITIONAL PROTECTION FOR IMAGES =============

document.addEventListener('DOMContentLoaded', function() {
    // Protect all images
    const images = document.getElementsByTagName('img');
    for (let i = 0; i < images.length; i++) {
        images[i].addEventListener('contextmenu', function(e) {
            e.preventDefault();
            return false;
        });
        
        images[i].addEventListener('dragstart', function(e) {
            e.preventDefault();
            return false;
        });
    }
});

// ============= EXPORT FOR TESTING =============

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        version: '1.0.0',
        name: 'AyurAI Veda Security System'
    };
}
