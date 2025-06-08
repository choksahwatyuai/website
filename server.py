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

        # Если запрошен корневой путь или конкретная страница
        try:
            # Определяем путь к файлу
            if self.path == '/':
                file_path = os.path.join(os.getcwd(), 'index.html')
            else:
                file_path = os.path.join(os.getcwd(), self.path.lstrip('/'))

            # Проверяем существование файла
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    if file_path.endswith('.html'):
                        self.send_header('Content-type', 'text/html; charset=utf-8')
                    elif file_path.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    elif file_path.endswith('.js'):
                        self.send_header('Content-type', 'application/javascript')
                    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                        self.send_header('Content-type', 'image/jpeg')
                    elif file_path.endswith('.png'):
                        self.send_header('Content-type', 'image/png')
                    self.end_headers()
                    self.wfile.write(file.read())
            else:
                self.send_error(404, 'File not found')
        except Exception as e:
            logger.error(f"Error serving {self.path}: {str(e)}")
            self.send_error(500, 'Internal Server Error')

    def do_POST(self):
        # Обработка webhook от Telegram
        if self.path == '/webhook':
            try:
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
                        
                        # Отправляем эхо-ответ для тестирования
                        api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                        response = requests.post(api_url, json={
                            'chat_id': chat_id,
                            'text': f"Получено сообщение: {text}"
                        })
                        logger.info(f"Bot response: {response.json()}")
                    except Exception as e:
                        logger.error(f"Error processing webhook data: {str(e)}")
                
            except Exception as e:
                logger.error(f"Error handling webhook: {str(e)}")
                self.send_error(500, 'Internal Server Error')
            return

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