#!/usr/bin/env python

from ws4py.client.threadedclient import WebSocketClient
import json
import fileinput
import ast
import uuid
import sys
import ast
import yaml

addr = 'ws://127.0.0.1:9217/ot/'


class DummyClient(WebSocketClient):

  def opened(self):
    #print('Opened up')
    pass

  def closed(self, code, reason=None):
    #print('Closed down', code, reason)
    pass

  def received_message(self, m):
    #m = m.data.decode("utf-8")
    #print(m[2:7])
    #if m[2:7] == 'order':
    print(m)


def openWs():
  ws = DummyClient(addr, protocols=['http-only'])
  ws.connect()
  return ws


def login():
  login = ['login', 'test', 'test']
  ws = openWs()
  ws.send(json.dumps(login))
  return ws


def test(ws, msg):
  ws.send(json.dumps(msg))


def test_limit_order(ws, msg):
  cmd = ['algo', 'new', 'TWAP', str(uuid.uuid4()), msg]
  print(cmd)
  ws.send(json.dumps(cmd))

def test_order_market(ws, msg):
  cmd = msg
  print(cmd)
  ws.send(json.dumps(cmd))

if __name__ == '__main__':
  try:
    ws = login()
    
    cmd = ['position', 12273, 'SIM']
    ws.send(json.dumps(cmd))

    ws.run_forever()
  except KeyboardInterrupt:
    ws.close()
