#!/usr/bin/env python
import os
import sys
import subprocess
import yaml
import re

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

#with open('test_cases.yml', 'r') as f:
#  TEST_CASES_DICT = yaml.safe_load(f)

#with open(TEST_LOG_FILE, 'r') as f:
#  TEST_LOG = yaml.safe_load(f)


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


def test_twap_order(msg, test_at):
  security = msg['Security']
  symbol = SECURITY_DICT[security['sec']]
  acc = security['acc'].lower()
  side = SIDE_DICT[security['side'].lower()]
  quantity = security['qty']
  min_size = msg['MinSize']
  price = msg['Price']
  valid_seconds = msg['ValidSeconds']
  if msg['Aggression'] == 'Highest':
    order_type = TYPE_DICT['market']
  else:
    order_type = TYPE_DICT['limit']
  tif = TIF_DICT['day']

  # New order single
  msg_type = 'D'
  # All FIX message for new ordersA
  cmd = '''awk -F, '$1 >= "{}" && /35={}/ && /55={}/ && /56={}/ && /54={}/ && /40={}/ && /59={}/' < {}'''.format(
      test_at, msg_type, symbol, acc, side, order_type, tif, FIX_LOG_FILE)

  out, err = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE).communicate()

  if out == '': return 'NOK'

  new_orders = out.strip().split('\n')
  total_quantity = 0

  for line in new_orders:
    field_val = parse_fix_field(line, str(38))
    if field_val is not None:
      total_quantity += int(field_val)
    else:
      return 'NOK'
  #print('Total new orders: {}'.format(total_quantity))

  # Execution report. Order may be canceled.
  msg_type = '8'
  # 39: identifies current status of order. If field value = 4, this order is canceled
  order_status = '4'
  cmd = '''awk -F, '$1 >= "{}" && /35={}/ && /55={}/ && /56=ot/ && /54={}/ && /40={}/ && /59={}/ && /39={}/' < {}'''.format(
      test_at, msg_type, symbol, side, order_type, tif, order_status,
      FIX_LOG_FILE)

  out, err = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE).communicate()

  canceled_orders = out.strip().split('\n')

  # Canceled order should not be counted into total quantity
  for o in canceled_orders:
    field_val = parse_fix_field(o, str(38))
    if field_val is not None:
      total_quantity -= int(field_val)

  #print('Total executed orders: {}'.format(total_quantity))
  if total_quantity != quantity:
    return 'NOK'

  return 'OK'


def parse_fix_field(msg, field_no):
  field_val_pairs = {}
  #print(msg.split('\x01'))
  for pair in msg.split('\x01'):
    if pair != '':
      field = pair.split('=')[0]
      val = pair.split('=')[1]
      field_val_pairs[field] = val

  #print(field_val_pairs)
  if field_no in field_val_pairs:
    return field_val_pairs[field_no]
  else:
    return None


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

  with open(order_file, 'r') as f:
    orders = yaml.safe_load(f)

  test_results = {}

  for key, val in order_log.items():
    msg = orders[key]['msg']
    algo = orders[key]['algo']
    test_at = val['place_order_at']

    ret = ''
    if algo == 'MANUAL':
      order_type = msg[4]
      if order_type == 'market':
        ret = test_manual_market_order(msg, test_at)
      elif order_type == 'limit':
        ret = test_manual_limit_order(msg, test_at)
    elif algo == 'TWAP':
      ret = test_twap_order(msg, test_at)

    test_results[key] = {}
    test_results[key]['result'] = ret
    print('{}. {} : {}'.format(ret, key, msg))

  test_result_file = order_file.split('.')[0] + '_results.yml'
  with open(test_result_file, 'w') as outfile:
    yaml.dump(test_results, outfile, default_flow_style=False)
