"""
AyurAI Veda - Dynamic Ayurvedic Theme Application
Run this file to start the Flask server
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from api.index import app

if __name__ == '__main__':
    print("=" * 60)
    print("🌿 AyurAI Veda - Time-Aware Ayurvedic Intelligence")
    print("=" * 60)
    print("\n✨ Starting Flask server...\n")
    print("📍 Access the application at:")
    print("   → http://127.0.0.1:5000/")
    print("   → http://localhost:5000/")
    print("\n🎨 Dynamic Theme System:")
    print("   → Vata Time: 4:00 AM - 10:00 AM (Morning)")
    print("   → Pitta Time: 10:00 AM - 2:00 PM (Midday)")
    print("   → Kapha Time: 6:00 PM - 10:00 PM (Evening)")
    print("\n⚡ Features:")
    print("   ✓ Time-aware backgrounds")
    print("   ✓ Glassmorphism UI")
    print("   ✓ Smooth animations")
    print("   ✓ Manual theme toggle")
    print("   ✓ Fully responsive")
    print("\n🔧 Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
