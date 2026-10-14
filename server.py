# Eventually change HTTPServer to ThreadingHTTPServer 

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = 'localhost'
serverPort = 8080
store = {}
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/plain")
        self.end_headers()

        key = self.path.lstrip("/")
        self.wfile.write(bytes(f"Requested key: {key}","utf-8"))
    def do_PUT(self):
        return None
if __name__ == "__main__":
    webServer = HTTPServer((hostName,serverPort),MyServer)
    print("Server started http://%s:%s" % (hostName,serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")



