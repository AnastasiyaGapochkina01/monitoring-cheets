import json
import requests
import requests_unixsocket

session = requests_unixsocket.Session()

# Формат URL для Unix-сокета
url = "http+unix://%2Fvar%2Frun%2Fdocker.sock/containers/json?all=true"
response = session.get(url)
containers = response.json()

lld_data = {"data": []}
for container in containers:
    lld_data["data"].append({
        "{#CONTAINER_ID}": container["Id"],
        "{#CONTAINER_NAME}": container["Names"][0].strip("/")
    })

print(json.dumps(lld_data))
