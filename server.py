from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import time, json, threading

hostName = 'localhost'
serverPort = 8080
store_lock = threading.Lock()
with open("disk.json", "r", encoding="utf-8") as file:
    store = json.load(file)

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

        response_body = {"value": value}
        self.wfile.write(json.dumps(response_body).encode("utf-8"))

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
            # Saving to disk:
            with open("disk.json", "w", encoding="utf-8") as file:
                json.dump(store, file, indent=4)
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
            # Saving to disk:
            print("Store after DEL",store)
            with open("disk.json", "w", encoding="utf-8") as file:
                json.dump(store, file, indent=4)
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

    # Because Benchmark expects POST I am reusing my PUT logic in the POST function
    def do_POST(self):
        return self.do_PUT()




    
if __name__ == "__main__":
    webServer = ThreadingHTTPServer((hostName,serverPort),MyServer)
    print("Server started http://%s:%s" % (hostName,serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")



