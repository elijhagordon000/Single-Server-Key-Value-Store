# Eventually change HTTPServer to ThreadingHTTPServer 

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import time, json

hostName = 'localhost'
serverPort = 8080
store = {"Eli":4}
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        key = self.path.lstrip("/")
        self.wfile.write(bytes(f"Requested key: {key}","utf-8"))
        self.wfile.write(bytes(f"Get value: {store[key]}", "utf-8"))
        return store[key]
    def do_PUT(self):
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        content_length = int(self.headers["Content-Length"])
        print('In put')
        key = self.path.lstrip("/")
        print(key)
        print("dict before",store)
        #Editing dictionary
        request_body = self.rfile.read(content_length)
        data  = json.loads(request_body)
        val = data["value"]
        store[key] = val
        print("dict after",store)
        # store[key] =  
        return None
    def do_DELETE(self):
        # Eventually do not send 200 message until error checking has been done
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        key = self.path.lstrip("/")
        print("deleting item: ", key)
        print(" dict before in del:", store)
        store.pop(key)
        print("dict after in del,", store)
        return None



    
if __name__ == "__main__":
    webServer = ThreadingHTTPServer((hostName,serverPort),MyServer)
    print("Server started http://%s:%s" % (hostName,serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")



