from flask import Flask, send_from_directory, jsonify, render_template_string
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
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return render_template_string(content)
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return "Error loading page", 500

@app.route('/<path:filename>')
def serve_file(filename):
    try:
        if filename.endswith('.html'):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return render_template_string(content)
        elif filename.endswith('.css'):
            return send_from_directory('.', filename, mimetype='text/css')
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.ico', '.jfif')):
            # Ищем файл в разных директориях
            possible_paths = ['.', 'images', 'backgrounds', 'kaligraf']
            for path in possible_paths:
                try:
                    if os.path.exists(os.path.join(path, filename)):
                        return send_from_directory(path, filename)
                except Exception:
                    continue
        return send_from_directory('.', filename)
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
    logger.info(f"Available files: {os.listdir('.')}")
    app.run(host='0.0.0.0', port=port) 