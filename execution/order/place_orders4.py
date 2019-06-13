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
total_executed = 0
algo_no = 0
algos = {}


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
    if 'algo' in m and ('teminated' in m or 'failed' in m):
      total_executed += 1
      print('total_excuted: {}'.format(total_executed))
      if total_executed == algo_no:
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
  print(cmd)

  ws.send(json.dumps(cmd))


def cancel_order_algo(ws, algo, action):
  log_file_handler.seek(0)
  log_lines = log_file_handler.readlines()
  print(log_lines)
  for line in log_lines:
    if 'algo' in line and 'new' in line:
      algo_id = line.strip().split(',')[2]
      msg = ['algo', 'cancel', int(algo_id)]
      print(msg)
      ws.send(json.dumps(msg))


def place_order(ws, msg):
  cmd = msg
  print(cmd)
  ws.send(json.dumps(cmd))


def cancel_orders(ws):
  log_file_handler.seek(0)
  log_lines = log_file_handler.readlines()
  print(log_lines)
  for line in log_lines:
    if 'order' in line and 'new' in line:
      order_id = line.strip().split(',')[1]
      msg = ['cancel', int(order_id)]
      print(msg)
      ws.send(json.dumps(msg))


def cancel_all_orders(ws, sec):
  msg = ['algo', 'cancel_all', int(sec), 'SIM']
  print(msg)
  ws.send(json.dumps(msg))


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
      action = val['action'].lower()
      msg = val['msg']
      #sec = msg['Security']['sec']
      #cancel_all_orders(ws, sec)
      #time.sleep(5)
      #algos[key] = {'orders':[]}

      if algo == 'manual':
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
        elif action == 'cancel':
          time.sleep(5)
          cancel_order_algo(ws, algo, action)

      place_order_at = (datetime.utcnow() - timedelta(seconds=1)).strftime('%Y%m%d-%H:%M:%S.%f')
      order_logs[key] = {'place_order_at': place_order_at}

    ws.run_forever()
  except KeyboardInterrupt:
    log_file_handler.close()
    ws.close()
