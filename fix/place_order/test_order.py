#!/usr/bin/env python
import os
import subprocess
import yaml

TEST_LOG_FILE = 'test_log.yml'

FIX_LOG_FILE = '/home/xzzzx/opentrade/store/fix/FIX.4.2-ot-sim.messages.current.log'

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


def parse_fix_order_market(val):

  test_time = val['test_time']
  symbol = val['symbol']
  acc, side, order_type, tif, quantity = convert_to_fix_fields(val)

  cmd = '''awk -F, '$1 >= "{}" && /35=D/ && /55={}/ && /56={}/ && /54={}/ && /40={}/ && /59={}/ && /38={}/' < {}'''.format(
      test_time, symbol, acc, side, order_type, tif, quantity, FIX_LOG_FILE)

  out, err = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE).communicate()

  ret = 'NOK' if out == '' else 'OK'

  return ret


def convert_to_fix_fields(val):
  acc = val['msg'][2].lower()

  side = SIDE_DICT[val['msg'][3].lower()]

  order_type = TYPE_DICT[val['msg'][4]]

  tif = TIF_DICT[val['msg'][5].lower()]

  quantity = str(val['msg'][6])

  return [acc, side, order_type, tif, quantity]


if __name__ == '__main__':

  with open(TEST_LOG_FILE, 'r') as f:
    execute_logs = yaml.safe_load(f)

  test_cases_ok = []
  test_cases_nok = []

  for key, val in execute_logs.items():
    print('Test case: {}'.format(key))
    print('WS msg: {}'.format(val))

    ret = ''
    if val['order_type'] == 'market':
      ret = parse_fix_order_market(val)

    if ret == '' or ret == 'NOK':
      test_cases_nok.append(key)
    else:
      test_cases_ok.append(key)

  print('OK: {}'.format(test_cases_ok))
  print('NOK: {}'.format(test_cases_nok))
