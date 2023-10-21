import argparse
import logging
from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_default_headers()
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_default_headers()
        self.end_headers()
        self.wfile.write(b'POST request received')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_default_headers()
        self.send_header('Allow', 'GET, POST, OPTIONS')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def send_default_headers(self):
        self.send_header('Access-Control-Allow-Origin', 'https://my-cool-site.com')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

def parse_args():
    parser = argparse.ArgumentParser(description='HTTP Server with command line arguments.')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Port number for the server')
    return parser.parse_args()

def setup_logging():
    logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def run(server_class=HTTPServer, handler_class=MyRequestHandler):
    args = parse_args()
    server_address = ('', args.port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {args.port}")
    logging.info(f"Starting server on port {args.port}")
    httpd.serve_forever()

if __name__ == '__main__':
    setup_logging()
    run()
