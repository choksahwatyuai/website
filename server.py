from flask import Flask, send_from_directory, jsonify, render_template_string
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

start_time = datetime.now()

def list_directory_contents():
    """Вспомогательная функция для вывода содержимого директории"""
    current_dir = os.getcwd()
    logger.info(f"Current working directory: {current_dir}")
    
    for root, dirs, files in os.walk(current_dir):
        logger.info(f"\nDirectory: {root}")
        if dirs:
            logger.info(f"Subdirectories: {dirs}")
        if files:
            logger.info(f"Files: {files}")

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
    logger.info("Attempting to serve index.html")
    try:
        # Проверяем наличие файла
        if not os.path.exists('index.html'):
            logger.error("index.html not found!")
            list_directory_contents()
            return "index.html not found", 404
            
        logger.info("Found index.html, attempting to read")
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info("Successfully read index.html")
        return content
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        list_directory_contents()
        return f"Error loading page: {str(e)}", 500

@app.route('/<path:filename>')
def serve_file(filename):
    logger.info(f"Attempting to serve: {filename}")
    try:
        if filename.endswith('.html'):
            if not os.path.exists(filename):
                logger.error(f"{filename} not found!")
                list_directory_contents()
                return f"{filename} not found", 404
                
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
            
        elif filename.endswith('.css'):
            return send_from_directory('.', filename, mimetype='text/css')
            
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.ico', '.jfif')):
            possible_paths = ['.', 'images', 'backgrounds', 'kaligraf']
            for path in possible_paths:
                full_path = os.path.join(path, filename)
                if os.path.exists(full_path):
                    logger.info(f"Found {filename} in {path}")
                    return send_from_directory(path, filename)
            
            logger.error(f"Image {filename} not found in any directory")
            list_directory_contents()
            return f"Image {filename} not found", 404
            
        return send_from_directory('.', filename)
    except Exception as e:
        logger.error(f"Error serving {filename}: {str(e)}")
        list_directory_contents()
        return f"Error: {str(e)}", 404

@app.errorhandler(404)
def not_found(e):
    logger.error(f"404 error: {e}")
    list_directory_contents()
    return "Page not found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info("Starting server...")
    list_directory_contents()
    app.run(host='0.0.0.0', port=port) 