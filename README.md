# Single-Server Key-Value Store

A simple single-server key-value store implemented in Python. The server supports concurrent client requests, in-memory key-value storage, JSON-based persistence, structured logging, and basic HTTP error handling.

## Features

- GET, PUT, POST, and DELETE operations
- Concurrent request handling with `ThreadingHTTPServer`
- Thread-safe access using a shared lock
- JSON-based disk persistence
- Structured request logging
- HTTP status codes for successful and failed requests
- Benchmark support for throughput, latency, correctness, and durability testing
- Data restoration after a server restart

## Project Overview

The key-value store uses a Python dictionary as its in-memory storage structure. Keys are provided through the request URL, while PUT and POST operations accept values through a JSON request body.

Example request body:

```json
{
  "value": "example_value"
}
```

PUT and DELETE operations update both the in-memory store and `disk.json`, allowing stored values to persist after the server is stopped and restarted.

Concurrency is handled using `ThreadingHTTPServer`, while a shared `threading.Lock()` protects the store from conflicting simultaneous operations.

## Requirements

- Python 3
- `requests` Python package for running the benchmark

Install the required package with:

```bash
python3 -m pip install requests
```

## How To Run

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Single-Server-Key-Value-Store
```

### 2. Verify `disk.json`

Make sure `disk.json` exists and contains valid JSON.

For an empty store:

```json
{}
```

### 3. Start the Server

```bash
python3 server.py
```

The server will start at:

```text
http://127.0.0.1:8080
```

Keep this terminal running while testing the server.

### 4. Run the Benchmark

Open a second terminal and run:

```bash
python3 benchmark.py
```

This performs both the SET and GET benchmark phases.

To run only the SET phase:

```bash
python3 benchmark.py set
```

To run only the GET phase:

```bash
python3 benchmark.py get
```

The GET-only benchmark can also be used after restarting the server to verify that data was successfully persisted to disk.

## Example Operations

### PUT

```bash
curl -X PUT http://127.0.0.1:8080/example \
-H "Content-Type: application/json" \
-d '{"value":"hello"}'
```

### GET

```bash
curl http://127.0.0.1:8080/example
```

### DELETE

```bash
curl -X DELETE http://127.0.0.1:8080/example
```

## Persistence

The server stores persistent data in:

```text
disk.json
```

PUT and DELETE operations update this file. When the server starts, the existing contents of `disk.json` are loaded back into memory.

## Demo

A video demonstration of the project, including GET, PUT, DELETE, concurrency, benchmarking, and persistence testing, is available here:

**YouTube Demo:** [https://youtu.be/LjjO4nTBKdI?si=-TiFnrkuellUPnhE]

## Future Improvements

Possible future improvements include:

- Database-backed persistence
- Authentication and authorization
- More detailed HTTP responses
- Per-key locking for improved concurrency
- Automated unit and integration testing
- Performance visualization for throughput and latency
- Multi-server replication and distributed storage support
