import socket
import sys
import os
import signal
import http.server
import socketserver


if len(sys.argv) < 2:
    port = int(input("Enter port number:"))
else:
    port = int(sys.argv[1])

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", port), handler) as server:
    print(f"Server started at http://localhost:{port}")
    server.serve_forever()
