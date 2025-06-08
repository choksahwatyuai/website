from flask import Flask, send_from_directory, jsonify
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

start_time = datetime.now()

@app.route('/health')
def health():
    uptime = (datetime.now() - start_time).total_seconds()
    return jsonify({
        'status': 'healthy',
        'uptime': uptime,
        'web_server': True,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 