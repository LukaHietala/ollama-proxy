import requests


input = input("Kysymys: ")

url = 'http://127.0.0.1:4321/api'
myobj = {}

myobj["content"] = input

x = requests.post(url, json = myobj)

print(x.json()["message"]["content"])