import urllib.request
from urllib.error import HTTPError
import json

try:
    response = urllib.request.urlopen("http://localhost:8080/api/city/Mumbai/area/Mumbai/forecast")
    print("Success:")
    print(response.read().decode())
except HTTPError as e:
    print("HTTPError:", e.code)
    try:
        print(json.loads(e.read().decode()))
    except:
        print(e.read().decode())
except Exception as e:
    print("Other error:", str(e))
