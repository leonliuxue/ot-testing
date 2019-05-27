#!/usr/bin/env python

import json
import requests
import time

url = 'http://103.224.167.234/api/'


def test():
  login = ['login', 'test', 'test']
  res = requests.post(url, data=json.dumps(login))
  res = json.loads(res.text)
  print(res)
  if res[1] == 'ok':
    session_token = res[2]['sessionToken']
  else:
    return
  print(session_token)
  securities = ['securities']
  res = requests.post(
      url,
      data=json.dumps(securities),
      headers={
          'session-token': session_token
      })
  res = json.loads(res.text)
  print(res)
  now = int(time.time())
  # ['OpenTick', security_id, interval, start_time, end_time]
  cmd = ['OpenTick', 12295, 1, now - 3600 * 24 * 5, now]
  res = requests.post(
      url,
      data=json.dumps(cmd),
      headers={
          'session-token': session_token
      })
  res = json.loads(res.text)
  print(res)



if __name__ == '__main__':
  test()
