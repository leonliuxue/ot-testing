#!/usr/bin/env python

from ws4py.client.threadedclient import WebSocketClient
import json
import fileinput
import ast
import uuid

addr = 'ws://127.0.0.1:9217/ot/'


class DummyClient(WebSocketClient):

  def opened(self):
    print('Opened up')

  def closed(self, code, reason=None):
    print('Closed down', code, reason)

  def received_message(self, m):
    # ["order", order_id, transaction_time, sequence_no, 'new', acc-order_id]
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
  print(msg)
  ws.send(json.dumps(msg))


if __name__ == '__main__':
  try:
    ws = login()

    ws.run_forever()
  except KeyboardInterrupt:
    ws.close()
