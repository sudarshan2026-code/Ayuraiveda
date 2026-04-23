from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
    <head><title>AyurAI Veda</title></head>
    <body style="background:#0a0a0a;color:#fff;text-align:center;padding:2rem;font-family:Arial;">
        <h1 style="color:#00D9FF;">🕉️ AyurAI Veda</h1>
        <h2>Ancient Wisdom. Intelligent Health.</h2>
        <div style="background:rgba(0,255,0,0.1);padding:1rem;margin:2rem;border-radius:8px;">
            <h3>✅ WORKING - No 500 Error!</h3>
        </div>
        <p>© 2026 AyurAI Veda - A Sudarshan Technologies Production</p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'AyurAI Veda'}

# This is the key for Vercel
app = app