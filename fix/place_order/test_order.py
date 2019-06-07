#!/usr/bin/env python
import os
import sys
import subprocess
import yaml

TEST_LOG_FILE = 'test_log.yml'
FIX_LOG_FILE = '/home/xzzzx/opentrade/store/fix/FIX.4.2-ot-sim.messages.current.log'
TEST_RESULTS_FILE = 'test_results.yml'

TIF_DICT = {
    'day': '0',
    'gtc': '1',
    'opg': '2',
    'ioc': '3',
    'fok': '4',
    'gtx': '5',
    'gtd': '6',
}

SIDE_DICT = {
    'buy': '1',
    'sell': '2',
    'buy minus': '3',
    'sell plus': '4',
    'sell short': '5',
    'sell short exempt': '6'
}

TYPE_DICT = {
    'market': '1',
    'limit': '2',
    'stop': '3',
    'stop limit': '4',
    'forex - swap': 'G',
}

with open('../../security.yml', 'r') as f:
  SECURITY_DICT = yaml.safe_load(f)

with open('test_cases.yml', 'r') as f:
  TEST_CASES_DICT = yaml.safe_load(f)

with open(TEST_LOG_FILE, 'r') as f:
  TEST_LOG = yaml.safe_load(f)


def test_manual_market_order(msg, test_at):
  symbol = SECURITY_DICT[msg[1]]

  acc, side, order_type, tif, quantity = convert_to_fix_fields(msg)

  cmd = '''awk -F, '$1 >= "{}" && /35=D/ && /55={}/ && /56={}/ && /54={}/ && /40={}/ && /59={}/ && /38={}/' < {}'''.format(
      test_at, symbol, acc, side, order_type, tif, quantity, FIX_LOG_FILE)

  out, err = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE).communicate()

  ret = 'NOK' if out == '' or err is not None else 'OK'

  return ret


def test_manual_limit_order(msg, test_at):
  symbol = SECURITY_DICT[msg[1]]

  acc, side, order_type, tif, quantity = convert_to_fix_fields(msg)

  cmd = '''awk -F, '$1 >= "{}" && /35=D/ && /55={}/ && /56={}/ && /54={}/ && /40={}/ && /59={}/ && /38={}/' < {}'''.format(
      test_at, symbol, acc, side, order_type, tif, quantity, FIX_LOG_FILE)

  out, err = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE).communicate()

  ret = 'NOK' if out == '' or err is not None else 'OK'

  return ret


def parse_fix_order_limit(msg, test_at):
  security = msg['Security']
  symbol = SECURITY_DICT[security['sec']]
  acc = security['acc'].lower()
  side = SIDE_DICT[security['side'].lower()]
  order_type = TYPE_DICT['market']
  tif = TIF_DICT['day']
  min_size = msg['MinSize']
  quantity = min_size

  #print([symbol, acc, side, order_type, tif, quantity])
  cmd = '''awk -F, '$1 >= "{}" && /35=D/ && /55={}/ && /56={}/ && /54={}/ && /40={}/ && /59={}/ && /38={}/' < {}'''.format(
      test_at, symbol, acc, side, order_type, tif, quantity, FIX_LOG_FILE)

  out, err = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE).communicate()

  ret = 'NOK' if out == '' or err is not None else 'OK'

  return ret


def convert_to_fix_fields(msg):
  acc = msg[2].lower()

  side = SIDE_DICT[msg[3].lower()]

  order_type = TYPE_DICT[msg[4]]

  tif = TIF_DICT[msg[5].lower()]

  quantity = str(msg[6])

  return [acc, side, order_type, tif, quantity]


if __name__ == '__main__':

  if len(sys.argv) == 1:
    print('Error. Order log file should be input argument.')
    exit()

  order_file = sys.argv[1]

  with open(order_file.split('.')[0] + '_log.yml') as f:
    order_log = yaml.safe_load(f)
    #print(order_log)

  with open(order_file, 'r') as f:
    orders = yaml.safe_load(f)
    #print(orders)

  test_cases_ok = []
  test_cases_nok = []
  test_results = {}

  for key, val in order_log.items():
    #print('Test case: {}'.format(key))

    msg = orders[key]['msg']
    #print('WS msg: {}'.format(msg))

    algo = orders[key]['algo']
    ret = ''
    test_at = val['place_order_at']

    if algo == 'MANUAL':
      order_type = msg[4]
      if order_type == 'market':
        ret = test_manual_market_order(msg, test_at)
      elif order_type == 'limit':
        ret = test_manual_limit_order(msg, test_at)
    elif algo == 'TWAP' and (order_log_file == 'all'
                             or order_log_file == 'limit'):
      pass

    if ret == '' or ret == 'NOK':
      test_cases_nok.append(key)
      #print('NOK')
      test_results[key] = {'result': 'NOK'}
    else:
      test_cases_ok.append(key)
      #print('OK')
      test_results[key] = {'result': 'OK'}
    print('{}. {} : {}'.format(ret, key, msg))

  test_result_file = order_file.split('.')[0] + '_results.yml'
  with open(test_result_file, 'w') as outfile:
    yaml.dump(test_results, outfile, default_flow_style=False)

  #print('OK: {}'.format(test_cases_ok))
  #print('NOK: {}'.format(test_cases_nok))
