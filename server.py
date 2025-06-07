from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
            return
        
        # Обработка остальных запросов
        if self.path == '/':
            self.path = '/index.html'
        
        try:
            with open(os.path.join(os.getcwd(), self.path.lstrip('/')), 'rb') as file:
                self.send_response(200)
                if self.path.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif self.path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif self.path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                self.wfile.write(file.read())
        except:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    run(port) 