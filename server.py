from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import time, json, threading

hostName = 'localhost'
serverPort = 8080
store_lock = threading.Lock()
store = {"Eli":4}
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        key = self.path.lstrip("/")
        store_lock.acquire()
        try:
            print("Acquired lock")
            value = store[key]
        except KeyError:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
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
                return

        store_lock.acquire()

        try:
            store[key] = val
            print(f"Dict after: {store}")

        finally:
            print("Releasing lock")
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
            print("Dict after delete",store)
        except KeyError:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
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



