from router import build_ring, nearest_server


# Same 1000 keys for both tests
test_keys = [f"key{i}" for i in range(1000)]


# -------------------------------
# Ring with 3 servers
# -------------------------------

servers_3 = [
    "localhost:8080",
    "localhost:8081",
    "localhost:8082"
]

ring_3 = build_ring(servers_3)

before_mapping = {}

for key in test_keys:
    before_mapping[key] = nearest_server(key, ring_3)


# -------------------------------
# Ring with 4 servers
# -------------------------------

servers_4 = [
    "localhost:8080",
    "localhost:8081",
    "localhost:8082",
    "localhost:8083"
]

ring_4 = build_ring(servers_4)

after_mapping = {}

for key in test_keys:
    after_mapping[key] = nearest_server(key, ring_4)


# -------------------------------
# Compare mappings
# -------------------------------

changed = 0
stayed = 0

for key in test_keys:

    if before_mapping[key] != after_mapping[key]:
        changed += 1

    else:
        stayed += 1


print("Total keys:", len(test_keys))
print("Keys that changed servers:", changed)
print("Keys that stayed on the same server:", stayed)

print(
    "Percentage changed:",
    (changed / len(test_keys)) * 100,
    "%"
)