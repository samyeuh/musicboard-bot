import os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

def keep_alive():
    HTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))), _Handler).serve_forever()

def start():
    threading.Thread(target=keep_alive, daemon=True).start()