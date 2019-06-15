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

    if ('\"algo\"' in m and 'done' not in m) or '\"order\"' in m:
      log_file_handler.write(m)
      log_file_handler.write('\n')
      log_file_handler.flush()


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


def cancel_order_algo(ws, algo, action):
  pass


def place_order(ws, msg):
  cmd = msg
  print(cmd)
  ws.send(json.dumps(cmd))


ws = None
order_log_file = None
log_file_handler = None

if __name__ == '__main__':
  try:
    if len(sys.argv) == 1:
      print('Error. Test case yaml file should be input argument.')
      exit()

    order_file = sys.argv[1]
    order_log_file = order_file.split('.')[0] + '.log'
    log_file_handler = open(order_log_file, 'w')
    log_file_handler.truncate()

    with open(order_file + '.yml', 'r') as f:
      orders = yaml.safe_load(f)

    ws = login()

    for key, val in orders.items():

      algo = val['algo']
      msg = val['msg']

      if algo == 'MANUAL':
        place_order(ws, msg)
      elif algo == 'TWAP':
        action = val['action']
        if action == 'new':
          place_order_algo(ws, algo, action, msg)
        elif action == 'cancel':
          cancel_order_algo(ws, algo, action)

      place_order_at = (datetime.utcnow() - timedelta(seconds=1)).strftime('%Y%m%d-%H:%M:%S.%f')
      order_logs[key] = {'place_order_at': place_order_at}

    ws.run_forever()
  except KeyboardInterrupt:
    log_file_handler.close()
    ws.close()
