#!/usr/bin/env python

import json
import requests
import time

url = 'http://103.224.167.234/api/'


def test():
  securities = ['securities']
  data = json.dumps(securities)
  res = requests.post(
    url,
    data=json.dumps(securities),
    )
  res = json.loads(res.text)
  print(res)

  login = ['login', 'test', 'test']
  # print(json.dumps(login))
  res = requests.post(url, data=json.dumps(login))
  # print(res)
  res = json.loads(res.text)
  print(res)
  if res[1] == 'ok':
    session_token = res[2]['sessionToken']
  else:
    return
  print(session_token)
  securities = ['securities']
  data = json.dumps(securities)
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

  data = json.dumps(cmd)
  res = requests.post(
      url,
      data=json.dumps(cmd),
      headers={
          'session-token': session_token
      })
  res = json.loads(res.text)
  print(res)

  cmd = [""]

  res = requests.post(
      url,
      data=json.dumps(cmd),
      headers={
          'session-token': session_token
      })
  res = json.loads(res.text)
  print(res)


  cmd = "h"
  print(json.dumps(cmd))
  res = requests.post(
      url,
      data=json.dumps(cmd),
      headers={
          'session-token': session_token
      })
  res = json.loads(res.text)
  print(res)

  cmd = ["bod"]
  print(json.dumps(cmd))
  res = requests.post(
      url,
      data=json.dumps(cmd),
      headers={
          'session-token': session_token
      })
  res = json.loads(res.text)
  print(res)

  # cmd = ['reconnect', 'kgi']
  # print(json.dumps(cmd))
  # res = requests.post(
  #     url,
  #     data=json.dumps(cmd),
  #     headers={
  #         'session-token': session_token
  #     })
  # res = json.loads(res.text)
  # print(res)

  cmd = ['position', 12285, 'KGI', True]
  print(json.dumps(cmd))
  res = requests.post(
    url,
    data=json.dumps(cmd),
    headers={
      'session-token': session_token
    })
  res = json.loads(res.text)
  print(res)


  cmd = ['target']
  print(json.dumps(cmd))
  res = requests.post(
    url,
    data=json.dumps(cmd),
    headers={
      'session-token': session_token
    })
  res = json.loads(res.text)
  print(res)


  cmd = ['target', 'KGI']
  print(json.dumps(cmd))
  res = requests.post(
    url,
    data=json.dumps(cmd),
    headers={
      'session-token': session_token
    })
  res = json.loads(res.text)
  print(res)

  cmd = ['target', 'xxKGI']
  print(json.dumps(cmd))
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
