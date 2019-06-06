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
  print(msg)
  ws.send(json.dumps(msg))


if __name__ == '__main__':
  try:
    ws = login()
    msg = ['order', 12273, 'SIM', 'Buy', 'limit', 'Day', 200, 1.3557, 0]
    #test(ws, msg)

    msg = [
        'algo', 'new', 'TWAP',
        str(uuid.uuid4()), {
            'Aggression': 'Highest',
            'InternalCross': None,
            'MaxPov': 0,
            'MinSize': 10,
            'Price': 0,
            'Security': {
                'acc': 'SIM',
                'qty': 100,
                'sec': 12273,
                'side': 'Buy'
            },
            'ValidSeconds': 300
        }
    ]
    test(ws, msg)

    ws.run_forever()
  except KeyboardInterrupt:
    ws.close()
