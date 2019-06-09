#!/usr/bin/env python

from ws4py.client.threadedclient import WebSocketClient
import json
import fileinput
import ast
import uuid
import sys
import ast
import yaml
from datetime import datetime, timedelta

WS_ADDRESS = 'ws://127.0.0.1:9217/ot/'
TEST_LOG_FILE = 'test_log.yml'

BROKER = {'103': 'sim'}


class DummyClient(WebSocketClient):

  def opened(self):
    #print('Opened up')
    pass

  def closed(self, code, reason=None):
    #print('Closed down', code, reason)
    pass

  def received_message(self, m):
    return

    m = m.data.decode("utf-8")
    if m[2, 7] != 'order' and m[2, 6] != 'algo': return
    print(m)

    m = ast.literal_eval(m.strip())
    #print(m)
    m = [i.strip() for i in m]
    if m[0] == 'order':
      if m[4] == 'unconfirmed':
        sec = m[5]
        acc = BROKER[m[8]]
        side = m[12]
        for key, order in orders.items():
          security = order['msg']['Security']
          if sec == security['sec'] and acc == security['acc'].lower(
          ) and side == security['side'].lower():
            if 'child_orders' not in order_logs[key]:
              order_logs[key]['child_orders'][m[1]] = {
                  'order_status': ['unconfirmed']
              }
      else:
        order_id = m[1]
        for key, log in order_logs.items():
          child_orders = log['child_orders']
          for child_order in child_orders:
            if order_id == child_order['order_id']:
              order_logs[key]

    elif m[0] == 'algo' and m[6] == 'iterminated':
      total_executed += 1
      if total_executed == len(orders):
        with open(order_file.split('.')[0] + '_log.yml', 'w') as outfile:
          yaml.dump(order_logs, outfile, default_flow_style=False)
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


order_logs = {}
orders = {}
total_executed = 0

if __name__ == '__main__':
  try:
    if len(sys.argv) == 1:
      print('Error. Test case yaml file should be input argument.')
      exit()

    ws = login()

    order_file = sys.argv[1]

    with open(order_file, 'r') as f:
      orders = yaml.safe_load(f)
      #order_logs = {}

    for key, val in orders.items():
      if key == 0:
        continue
      algo = val['algo']
      msg = val['msg']

      if algo == 'MANUAL':
        place_order(ws, msg)
        #order_logs[key] = {
        #    'place_order_at':
        #    datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3],
        #}
      elif algo == 'TWAP':
        place_order_algo(ws, algo, msg)
      
      order_logs[key] = {
            'place_order_at':
            (datetime.utcnow() - timedelta(seconds=1)).strftime('%Y%m%d-%H:%M:%S.%f')[:-3],
        }

    with open(order_file.split('.')[0] + '_log.yml', 'w') as outfile:
      yaml.dump(order_logs, outfile, default_flow_style=False)

    #ws.run_forever()
  except KeyboardInterrupt:
    ws.close()
