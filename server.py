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
        
        # Если запрошен корневой путь, отдаем index.html
        if self.path == '/':
            self.path = '/index.html'
        
        # Обработка остальных запросов
        try:
            file_path = os.path.join(os.getcwd(), self.path.lstrip('/'))
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    if self.path.endswith('.html'):
                        self.send_header('Content-type', 'text/html')
                    elif self.path.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    elif self.path.endswith('.js'):
                        self.send_header('Content-type', 'application/javascript')
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