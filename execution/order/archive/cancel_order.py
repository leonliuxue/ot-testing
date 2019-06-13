#!/usr/bin/env python

import json
import sys
import uuid
from datetime import datetime, timedelta

import yaml
from ws4py.client.threadedclient import WebSocketClient

WS_ADDRESS = 'ws://127.0.0.1:9217/ot/'
TEST_LOG_FILE = 'test_log.yml'

BROKER = {'103': 'sim'}
order_logs = {}
orders = {}
total_executed = 0


class DummyClient(WebSocketClient):

  def opened(self):
    # print('Opened up')
    pass

  def closed(self, code, reason=None):
    # print('Closed down', code, reason)
    pass

  def received_message(self, m):
    global total_executed
    m = m.data.decode("utf-8")

    print(m)
    if 'teminated' in m:
      total_executed += 1
      print('total_excuted: {}'.format(total_executed))
      if total_executed == len(order_logs):
        ws.close()
        exit()


def openWs():
  ws = DummyClient(WS_ADDRESS, protocols=['http-only'])
  ws.connect()
  return ws


def login():
  login = ['login', 'test', 'test']
  ws = openWs()
  ws.send(json.dumps(login))
  return ws


def place_order_algo(ws, algo, action, msg):
  cmd = ['algo', action, algo, str(uuid.uuid4()), msg]
  print(cmd)
  ws.send(json.dumps(cmd))


def place_order(ws, msg):
  cmd = msg
  print(cmd)
  ws.send(json.dumps(cmd))


ws = None
if __name__ == '__main__':
  try:
    ws = login()

    if len(sys.argv) == 1:
      print('Error. Algo id should be input argument.')
      exit()

    if sys.argv[1] == 'algo':
      msg = ['algo', 'cancel', int(sys.argv[3])]
    elif sys.argv[1] == 'cancel':
      msg = ['cancel', int(sys.argv[2])]
    else:
      print('Error msg: {}'.format(sys.argv))
      exit()

    print(msg)

    ws.send(json.dumps(msg))

  except KeyboardInterrupt:
    ws.close()
