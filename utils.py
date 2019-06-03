import json

import requests
import yaml

is_skip = True

with open("golden_cases.yaml", 'r') as stream:
  try:
    ret = yaml.safe_load(stream)
    print()
  except yaml.YAMLError as exc:
    print(exc)

config = ret['config']
test_cases_all = ret['tests']

url = config['url']
login = config['login']
res = requests.post(url, data=json.dumps(login))
res = json.loads(res.text)
if res[1] == 'ok':
  session_token = res[2]['sessionToken']
else:
  exit(1)
