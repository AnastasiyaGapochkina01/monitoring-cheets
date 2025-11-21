import sys
import requests
import requests_unixsocket

container_id = sys.argv[1]
metric = sys.argv[2]  # Например: status, cpu, memory

session = requests_unixsocket.Session()
url = f"http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/{container_id}/stats?stream=false"
response = session.get(url)
stats = response.json()

if metric == "status":
    url_info = f"http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/{container_id}/json"
    info = session.get(url_info).json()
    print(info["State"]["Status"])

elif metric == "cpu":
    cpu_usage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
    print(cpu_usage)

elif metric == "memory":
    memory_usage = stats["memory_stats"]["usage"]
    print(memory_usage)


