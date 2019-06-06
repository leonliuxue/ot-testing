#!/usr/bin/env python
import os
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


def parse_fix_order_market(msg, test_at):
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

  print([symbol, acc, side, order_type, tif, quantity])
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

  with open(TEST_LOG_FILE, 'r') as f:
    test_log = yaml.safe_load(f)

  test_cases_ok = []
  test_cases_nok = []

  test_results = {}
  for key, val in test_log.items():
    print('Test case: {}'.format(key))

    msg = TEST_CASES_DICT[key]['msg']
    print('WS msg: {}'.format(msg))

    algo = TEST_CASES_DICT[key]['algo']
    ret = ''
    test_at = val['test_at']
    if algo == 'MANUAL':
      order_type = msg[4]
      if order_type == 'market':   
        ret = parse_fix_order_market(msg, test_at)
      elif order_type == 'limit':
          pass
    elif algo == 'TWAP':
        pass

    #if order_type == 'market':
    #  ret = parse_fix_order_market(msg, test_at)
    #elif order_type == 'limit':
    #  ret = parse_fix_order_limit(msg, test_at)

    if ret == '' or ret == 'NOK':
      test_cases_nok.append(key)
      print('NOK')
      test_results[key] = {'result': 'NOK'}
    else:
      test_cases_ok.append(key)
      print('OK')
      test_results[key] = {'result': 'OK'}

  with open(TEST_RESULTS_FILE, 'w') as outfile:
    yaml.dump(test_results, outfile, default_flow_style=False)

  print('OK: {}'.format(test_cases_ok))
  print('NOK: {}'.format(test_cases_nok))
