import http.server
import socketserver
import json

class MeinHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response = json.dumps({"status": "healthy", "message": "Simple server working!"})
            self.wfile.write(response.encode())
        else:
            self.send_response(200)
            self.send_header("Content-type", "application/json") 
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response = json.dumps({"message": "Hello from simple server!", "path": self.path})
            self.wfile.write(response.encode())

PORT = 8000

with socketserver.TCPServer(("", PORT), MeinHandler) as httpd:
    print("✅ Simple server running on port " + str(PORT))
    print("🌐 Test with: curl http://localhost:" + str(PORT) + "/api/health")
    httpd.serve_forever()
