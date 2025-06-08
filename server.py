from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import logging
import requests

# Настраиваем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "ok"}
            self.wfile.write(json.dumps(response).encode())
            return
        elif self.path == '/webhook':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"ok": True}
            self.wfile.write(json.dumps(response).encode())
            return

    def do_POST(self):
        if self.path == '/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Отправляем 200 OK сразу
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
            
            # Логируем полученные данные
            logger.info(f"Received webhook data: {post_data.decode('utf-8')}")
            
            # Пересылаем данные боту
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            if bot_token:
                try:
                    webhook_data = json.loads(post_data.decode('utf-8'))
                    chat_id = webhook_data['message']['chat']['id']
                    text = webhook_data['message']['text']
                    
                    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    response = requests.post(api_url, json={
                        'chat_id': chat_id,
                        'text': f"Получено сообщение: {text}"
                    })
                    logger.info(f"Bot response: {response.json()}")
                except Exception as e:
                    logger.error(f"Error processing webhook data: {str(e)}")

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logger.info(f'Starting server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('Shutting down server...')
        httpd.server_close()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    run(port) 