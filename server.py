from flask import Flask, send_from_directory, jsonify, render_template
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
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return "Error loading page", 500

@app.route('/<path:filename>')
def serve_file(filename):
    try:
        if filename.endswith('.html'):
            return render_template(filename)
        return send_from_directory('static', filename)
    except Exception as e:
        logger.error(f"Error serving {filename}: {e}")
        return "File not found", 404

@app.errorhandler(404)
def not_found(e):
    logger.error(f"404 error: {e}")
    return "Page not found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting server on port {port}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Files in static: {os.listdir('static')}")
    logger.info(f"Files in templates: {os.listdir('templates')}")
    app.run(host='0.0.0.0', port=port) 