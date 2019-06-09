#!/usr/bin/env python

from ws4py.client.threadedclient import WebSocketClient
import json
import fileinput
import ast
import uuid
import sys
import ast
import yaml
from datetime import datetime

WS_ADDRESS = 'ws://127.0.0.1:9217/ot/'
TEST_LOG_FILE = 'test_log.yml'


class DummyClient(WebSocketClient):

  def opened(self):
    #print('Opened up')
    pass

  def closed(self, code, reason=None):
    #print('Closed down', code, reason)
    pass

  def received_message(self, m):
    m = m.data.decode("utf-8")
    #print(m[2:7])
    #if m[2:7] == 'order':
    #print(m)
    pass


def openWs():
  ws = DummyClient(WS_ADDRESS, protocols=['http-only'])
  ws.connect()
  return ws


def login():
  login = ['login', 'test', 'test']
  ws = openWs()
  ws.send(json.dumps(login))
  return ws


def test(ws, msg):
  ws.send(json.dumps(msg))


def place_order_algo(ws, algo, msg):
  cmd = ['algo', 'new', algo, str(uuid.uuid4()), msg]
  print(cmd)
  ws.send(json.dumps(cmd))


def place_order(ws, msg):
  cmd = msg
  print(cmd)
  ws.send(json.dumps(cmd))


if __name__ == '__main__':
  try:
    if len(sys.argv) == 1:
      print('Error. Test case yaml file should be input argument.')
      exit()

    ws = login()

    order_file = sys.argv[1]

    with open(order_file, 'r') as f:
      orders = yaml.safe_load(f)

    order_logs = {}

    for key, val in orders.items():
      algo = val['algo']
      msg = val['msg']

      if algo == 'MANUAL':
        place_order(ws, msg)
        order_logs[key] = {
            'place_order_at':
            datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3],
        }
      elif algo == 'TWAP':
        place_order_algo(ws, algo, msg)
        order_logs[key] = {
            'place_order_at':
            datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3],
        }

    with open(order_file.split('.')[0] + '_log.yml', 'w') as outfile:
      yaml.dump(order_logs, outfile, default_flow_style=False)

    #ws.run_forever()
  except KeyboardInterrupt:
    ws.close()
