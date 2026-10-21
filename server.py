from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import time, json, threading

hostName = 'localhost'
serverPort = 8080
store_lock = threading.Lock()
store = {"Eli":4}
class MyServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return
    def log_operation(self, operation, key,  status_code):
        timestamp = time.strftime("%Y-%-m-%d %H:%M:%S")

        if status_code == 200:
            result = "SUCCESS"
        else:
            result = "FAILED"
        print(f"{timestamp} | {operation} | key = {key} | {result} | {status_code}")

    def do_GET(self):
        key = self.path.lstrip("/")
        store_lock.acquire()
        try:
            value = store[key]
            self.log_operation("GET", key, 200)
        except KeyError:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.log_operation("GET", key, 404)
            return
        finally:
            store_lock.release()

        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()

        self.wfile.write(bytes(f"Get value: {value}", "utf-8"))

    def do_PUT(self):
        # Key managing:
        key = self.path.lstrip("/")
    
        try:
            content_length = int(self.headers["Content-Length"])
            request_body = self.rfile.read(content_length)
            data  = json.loads(request_body)
            val = data["value"]
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.log_operation("PUT", key, 400)
                return

        store_lock.acquire()

        try:
            store[key] = val
            self.log_operation("PUT", key, 200)

        finally:
            store_lock.release()
        
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()

    def do_DELETE(self):
        # Eventually do not send 200 message until error checking has been done
        key = self.path.lstrip("/")
        store_lock.acquire()  
        try:
            store.pop(key)
            self.log_operation("DEL", key, 200)
        except KeyError:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.log_operation("DEL", key, 404)
            return
        finally:
            store_lock.release()

        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()




    
if __name__ == "__main__":
    webServer = ThreadingHTTPServer((hostName,serverPort),MyServer)
    print("Server started http://%s:%s" % (hostName,serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")



