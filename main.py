import socket
import sys
import os
import signal
import http.server
import socketserver
import asyncio
import websockets
import json
import threading


connected_clients = set()

async def handle_client(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received from client: {message}")

            # Example: Echo back with JSON
            response = {
                "type": "echo",
                "message": message
            }

        for client in connected_clients:
            await client.send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(websocket)

async def websocket_server(port):
    async with websockets.serve(handle_client, "0.0.0.0", port):
        print("WebSocket server running on ws://localhost:", port)
        await asyncio.Future()  # Run forever

def start_http_server(port):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as server:
        print(f"Server started at http://localhost:{port}")
        server.serve_forever()

def main():
    if len(sys.argv) >= 3:
        http_port = int(sys.argv[1])
        ws_port = int(sys.argv[2])
    else:
        http_port = 8000
        ws_port = 8765


    http_thread = threading.Thread(
        target=start_http_server,
        args=(http_port,),
        daemon=True
    )

    http_thread.start()

    # Run websocket server
    asyncio.run(websocket_server(ws_port))


if __name__ == "__main__":
    main()

