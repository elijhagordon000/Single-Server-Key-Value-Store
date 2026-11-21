from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import requests
import hashlib




def deterministic_hash(text: str) -> int:
    return int(
        hashlib.sha256(text.encode("utf-8")).hexdigest(),
        16
    )


ring_size = 100000
virtual_nodes_per_server = 100



# Build consistent hash ring


def build_ring(servers):
    server_list = []

    for server in servers:

        # Original physical server position
        server_position = deterministic_hash(server) % ring_size
        server_list.append((server_position, server))

        # Virtual nodes
        for i in range(1, virtual_nodes_per_server):
            virtual_node = f"{server}_vn{i}"

            vn_position = (
                deterministic_hash(virtual_node) % ring_size
            )

            # Store physical server as the owner
            server_list.append((vn_position, server))

    # Sort by ring position
    server_list.sort()

    return server_list



# Physical KV servers


servers = [
    "localhost:8080",
    # "localhost:8081",
    # "localhost:8082"
]

server_list = build_ring(servers)



# Find server responsible for a key


def nearest_server(key, ring):
    hashed_key = deterministic_hash(key) % ring_size

    # Move clockwise through ring
    for server_position, server in ring:
        if server_position >= hashed_key:
            return server

    # Wrap around
    return ring[0][1]



class RouterHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        key = self.path.lstrip("/")

        selected_server = nearest_server(
            key,
            server_list
        )

        print("GET Key:", key)
        print("Selected server:", selected_server)

        url = f"http://{selected_server}/{key}"

        response = requests.get(url)

        # Return backend response to client
        self.send_response(response.status_code)

        self.send_header(
            "Content-Type",
            response.headers.get(
                "Content-Type",
                "text/plain"
            )
        )

        self.end_headers()

        self.wfile.write(response.content)


    def do_PUT(self):
        key = self.path.lstrip("/")

        selected_server = nearest_server(
            key,
            server_list
        )

        print("PUT Key:", key)
        print("Selected server:", selected_server)

        # Read request body
        content_length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(content_length)

        url = f"http://{selected_server}/{key}"

        # Forward PUT to backend
        response = requests.put(
            url,
            data=body,
            headers={
                "Content-Type": "application/json"
            }
        )

        # Return backend response to client
        self.send_response(response.status_code)

        self.send_header(
            "Content-Type",
            response.headers.get(
                "Content-Type",
                "text/plain"
            )
        )

        self.end_headers()

        self.wfile.write(response.content)




    def do_DELETE(self):
        key = self.path.lstrip("/")

        selected_server = nearest_server(
            key,
            server_list
        )

        print("DELETE Key:", key)
        print("Selected server:", selected_server)

        url = f"http://{selected_server}/{key}"

        # Forward DELETE to backend
        response = requests.delete(url)

        # Return backend response to client
        self.send_response(response.status_code)

        self.send_header(
            "Content-Type",
            response.headers.get(
                "Content-Type",
                "text/plain"
            )
        )

        self.end_headers()

        self.wfile.write(response.content)

    def do_POST(self):
        return self.do_PUT()





if __name__ == "__main__":

    router_port = 9000

    print("Physical servers:")
    for server in servers:
        print(server)

    print(
        "Total ring positions:",
        len(server_list)
    )

    router = ThreadingHTTPServer(
        ("0.0.0.0", router_port),
        RouterHandler
    )

    print(
        f"Router started on http://localhost:{router_port}"
    )

    router.serve_forever()