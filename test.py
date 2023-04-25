import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE+"video/55",data={"name":"Naveena is a bad ass","likes":0,"views":2})
print(response.json())

response = requests.get(BASE+"video/55")
print(response.json())

response = requests.patch(BASE+"video/55",data={"likes":8888,"views":200000000})
print(response.json())

response = requests.delete(BASE+"video/55")
print(response)