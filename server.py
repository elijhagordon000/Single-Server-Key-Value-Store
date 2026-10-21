# Eventually change HTTPServer to ThreadingHTTPServer 

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import time, json, threading

hostName = 'localhost'
serverPort = 8080
store_lock = threading.Lock()
store = {"Eli":4}
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        key = self.path.lstrip("/")
        print("Waiting for lock")
        store_lock.acquire()
        
        try:
            print("Acquired lock")
            value = store[key]
        except:
            print("Key error in GET")
        finally:
            print("Releasing Lock")
            store_lock.release()
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()

        self.wfile.write(bytes(f"Requested key: {key}","utf-8"))
        self.wfile.write(bytes(f"Get value: {value}", "utf-8"))

    def do_PUT(self):
        # Key managing:
        key = self.path.lstrip("/")
        content_length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(content_length)
        data  = json.loads(request_body)
        val = data["value"]
        print("Waiting for lock")
        store_lock.acquire()
        try:
            print("Acquired Lock")
            store[key] = val
            print("dict after",store)
        except:
            print("Key Error in PUT")
        finally:
            print("Releasing lock")
            store_lock.release()
        # Implement error handling eventually
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        return None
    def do_DELETE(self):
        # Eventually do not send 200 message until error checking has been done
        key = self.path.lstrip("/")
        store_lock.acquire()
        print("Dict before delete",store)
        try:
            store.pop(key)
            print("Dict after delete",store)
        except:
            print("Key Errror in DEL")
        finally:
            store_lock.release()

        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        
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



