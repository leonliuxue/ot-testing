import json

import requests
r = requests.get('https://api.github.com/events')
print(r)


login = ['login', 'test', 'test']
j = json.dumps(login)
# print(j['login'])
print()

# A dictionary of roll numbers vs student names

studentDict = {1: "John Napier",

               2: "Leonhard Euler",

               3: "Scarlett O'Hara",

               4: "Henry Ford"}

jsonString = json.dumps(studentDict)

# A python dictionary as a JSON string

print(jsonString)

print()

