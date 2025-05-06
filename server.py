import socket
import os
import datetime
import threading

HOST = 'localhost'
PORT = 8080
WEB_ROOT = './www'

MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.jpg': 'image/jpeg',
}

def log_request(method, path, code): # Log the request to a file
    with open("log.txt", "a") as log:
        log.write(f"{datetime.datetime.now()} - {method} {path} -> {code}\n")

def get_mime_type(file_path): # Get the MIME type based on the file extension
    ext = os.path.splitext(file_path)[1]
    return MIME_TYPES.get(ext.lower(), 'application/octet-stream')

def handle_request(conn, addr): # Handle incoming requests
    try:
        # Receive the request from the client
        request = conn.recv(1024).decode()
        if not request:
            return

        parts = request.split()
        # Ensure it's a valid HTTP GET request
        if len(request.split()) < 2 or request.split()[0] != 'GET':
            raise IOError
        
        method, path = parts[0], parts[1]
        print(f"[{addr}] Request: {method} {path}")

        # Default to index.html if the root is requested
        if path == '/':
            path = '/index.html'

        # Get the file path
        file_path = os.path.join(WEB_ROOT, path.lstrip('/'))
        print(f"File path requested: {file_path}")

        # Check if the requested file exists
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error opening file {file_path}: {e}")
                return

            mime_type = get_mime_type(file_path)
            headers = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {mime_type}\r\n"
                f"Content-Length: {len(content)}\r\n"
                "Connection: close\r\n"
                "Cache-Control: no-cache, no-store, must-revalidate\r\n"
                "Pragma: no-cache\r\n"
                "Expires: 0\r\n"
                "\r\n"
            ).encode()

            # Send the response
            conn.sendall(headers + content)
            # Log the successful request
            log_request(method, path, 200)
        else:
            # If the file does not exist, send a 404 error
            error_html = b"""
            <html>
                <head><title>Error 404</title></head>
                <body style="background-color: #fdd;">
                    <h1>404 - Page Not Found</h1>
                    <p>The requested file does not exist on the server.</p>
                </body>
            </html>
            """
            # Set the content type to HTML
            headers = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(error_html)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).encode()

            # Send the 404 response
            conn.sendall(headers + error_html)
            # Log the 404 error
            log_request(method, path, 404)

    except Exception as e:
        print(f"Error handling request from {addr}: {e}") # Log any exceptions
    finally:
        conn.close() # Ensure the connection is closed

def start_server():
    # Create the server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print(f"Server listening on http://{HOST}:{PORT}")

        # Loop to accept incoming connections
        while True:
            conn, addr = server_socket.accept() # Accept a connection
            thread = threading.Thread(target=handle_request, args=(conn, addr)) # Create a new thread for each connection
            thread.start() # Start the thread to handle the request

if __name__ == "__main__":
    start_server()
