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


def place_limit_order(ws, algo, msg):
  cmd = ['algo', 'new', algo, str(uuid.uuid4()), msg]
  print(cmd)
  ws.send(json.dumps(cmd))


def place_order_market(ws, msg):
  cmd = msg
  print(cmd)
  ws.send(json.dumps(cmd))


if __name__ == '__main__':
  try:
    if len(sys.argv) == 1:
      print('Error. Test case yaml file should be input argument.')
      exit()

    ws = login()

    tc_file = sys.argv[1]

    with open(tc_file, 'r') as f:
      ret = yaml.safe_load(f)

    test_log = {}
    for key, val in ret.items():
      msg = val['msg']
      order_type = val['order_type'] 

      if order_type == 'limit':
        algo = val['algo']
        place_limit_order(ws, algo, msg)
        test_log[key] = {
            'test_at': datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3],
        }

      #elif order_type == 'market':
      #  place_order_market(ws, msg)
      #  test_log[key] = {'test_at': datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3], }

    with open(TEST_LOG_FILE, 'w') as outfile:
      yaml.dump(test_log, outfile, default_flow_style=False)

    #ws.run_forever()
  except KeyboardInterrupt:
    ws.close()
