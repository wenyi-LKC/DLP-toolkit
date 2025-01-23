from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

class SimpleHTTPServer(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the length of the data
        content_length = int(self.headers['Content-Length'])
        # Read the POST data
        post_data = self.rfile.read(content_length)
        
        # Ensure the "exfil" directory exists
        save_dir = "exfil"
        os.makedirs(save_dir, exist_ok=True)
        
        # Generate a filename based on the current timestamp
        filename = os.path.join(save_dir, time.strftime("%Y%m%d-%H%M%S.txt"))
        
        # Write the data to the file
        with open(filename, 'wb') as file:
            file.write(post_data)
        
        # Respond to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Data saved to file: " + filename.encode())

if __name__ == "__main__":
    server_address = ('', 8787)  # Listen on all interfaces, port 8787
    httpd = HTTPServer(server_address, SimpleHTTPServer)
    print("Starting server on port 8787...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()
