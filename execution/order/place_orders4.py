#!/usr/bin/env python

import json
import sys
import uuid
from datetime import datetime, timedelta
import time
import yaml
from ws4py.client.threadedclient import WebSocketClient

WS_ADDRESS = 'ws://127.0.0.1:9217/ot/'
TEST_LOG_FILE = 'test_log.yml'

BROKER = {'103': 'sim'}
order_logs = {}
orders = {}
algo_no = 0
algos = {}


class DummyClient(WebSocketClient):
  total_executed = 0

  def opened(self):
    # print('Opened up')
    pass

  def closed(self, code, reason=None):
    # print('Closed down', code, reason)
    pass

  def received_message(self, m):
    m = m.data.decode("utf-8")

    print(m)

    if 'algo' in m and ('teminated' in m or 'failed' in m):
      algo_id = m.strip()[1:-1].split(',')[2]
      self.total_executed += 1
      print('{},{}'.format(algo_id, 'filled'))
      if self.total_executed == algo_no:
        #time.sleep(5)
        ws.close()
        exit()

    if ('\"order\"' in m or '\"algo\"' in m) and 'done' not in m:
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
  #print(cmd)

  ws.send(json.dumps(cmd))


def place_order(ws, msg):
  cmd = msg
  #print(cmd)
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
    log_file_handler = open(order_log_file, 'a+')
    log_file_handler.truncate()

    with open(order_file + '.yml', 'r') as f:
      orders = yaml.safe_load(f)

    ws = login()

    for key, val in orders.items():
      algo = val['algo']
      action = val['action']
      msg = val['msg']
      if algo == 'MANUAL':
        if action == 'new':
          place_order(ws, msg)
        elif action == 'cancel':
          time.sleep(5)
          cancel_orders(ws)
      elif algo == 'TWAP':
        action = val['action']
        if action == 'new':
          algo_no += 1
          place_order_algo(ws, algo, action, msg)

    ws.run_forever()
  except KeyboardInterrupt:
    log_file_handler.close()
    ws.close()
