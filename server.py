from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json

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
            print(f"Error serving {self.path}: {str(e)}")
            self.send_error(500, 'Internal Server Error')

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Starting server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down server...')
        httpd.server_close()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    run(port) 