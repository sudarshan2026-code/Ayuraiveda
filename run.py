"""
AyurAI Veda - Run Flask Server
"""
import sys
import os

# Fix Unicode output on Windows terminals
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from api.index import app

if __name__ == '__main__':
    print("=" * 50)
    print("AyurAI Veda - Flask Server")
    print("=" * 50)
    print("Access at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
