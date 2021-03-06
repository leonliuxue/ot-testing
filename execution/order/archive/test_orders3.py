#!/usr/bin/env python
import subprocess
import sys

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

SIDE_DICT = {'buy': '1', 'sell': '2', 'buy minus': '3', 'sell plus': '4', 'sell short': '5', 'sell short exempt': '6'}

TYPE_DICT = {
    'market': '1',
    'limit': '2',
    'stop': '3',
    'stop limit': '4',
    'forex - swap': 'G',
}

with open('../../security.yml', 'r') as f:
  SECURITY_DICT = yaml.safe_load(f)


def test_manual_market_order(msg, test_at):
  symbol = SECURITY_DICT[msg[1]]
  acc, side, order_type, tif, quantity = convert_to_fix_fields(msg)

  cmd = '''awk -F, '$1 >= "{}" && /35=D/ && /55={}/ && /56={}/ && /54={}/ && /40={}/ && /59={}/ && /38={}/' < {}'''.format(
      test_at, symbol, acc, side, order_type, tif, quantity, FIX_LOG_FILE)
  out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
  ret = 'NOK' if out == '' or err is not None else 'OK'

  return ret


def test_manual_limit_order(msg, test_at):
  symbol = SECURITY_DICT[msg[1]]
  acc, side, order_type, tif, quantity = convert_to_fix_fields(msg)

  cmd = '''awk -F, '$1 >= "{}" && /35=D/ && /55={}/ && /56={}/ && /54={}/ && /40={}/ && /59={}/ && /38={}/' < {}'''.format(
      test_at, symbol, acc, side, order_type, tif, quantity, FIX_LOG_FILE)
  out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
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
  out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
  if out == '': return 'NOK'

  total_quantity = 0

  new_orders = out.strip().split('\n')
  for line in new_orders:
    field_val = parse_fix_field(line, str(38))
    if field_val is not None:
      total_quantity += int(field_val)
  # print('Total new orders: {}'.format(total_quantity))

  # Execution report. Order may be canceled.
  msg_type = '8'
  # 39: identifies current status of order. If field value = 4, this order is canceled
  order_status = '4'
  cmd = '''awk -F, '$1 >= "{}" && /35={}/ && /55={}/ && /56=ot/ && /54={}/ && /40={}/ && /59={}/ && /39={}/' < {}'''.format(
      test_at, msg_type, symbol, side, order_type, tif, order_status, FIX_LOG_FILE)
  out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()

  canceled_orders = out.strip().split('\n')
  # Canceled order should not be counted into total quantity
  for o in canceled_orders:
    field_val = parse_fix_field(o, str(38))
    if field_val is not None:
      total_quantity -= int(field_val)

  # print('Total executed orders: {}'.format(total_quantity))
  if total_quantity != quantity:
    return 'NOK'

  return 'OK'


def get_fix_msg(msg_type, order_id):
  # New order single
  # msg_type = 'D'
  # All FIX message for new ordersA
  cmd = '''tail -10000 {} | awk '/35={}/ && /11={}/' '''.format(FIX_LOG_FILE, msg_type, order_id)
  out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()

  return out


def parse_fix_field(msg, field_no):

  field_val_pairs = {}
  # print(msg.split('\x01'))
  for pair in msg.strip().split('\x01'):
    if pair != '':
      field = pair.split('=')[0]
      val = pair.split('=')[1]
      field_val_pairs[field] = val

  # print(field_val_pairs)
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
  with open(order_file + '.log') as f:
    log_lines = f.readlines()

  algos = {}

  for line in log_lines:
    if 'algo' in line and 'new' in line:
      line = line.strip()[1:-1]
      tokens = line.split(',')
      algo_id = tokens[2]
      exec_tm = tokens[3]
      algos[algo_id] = {}

      quantity = 0
      m = re.search(r'qty\\(.+?),', line)
      if m:
        quantity = float(m.group(1).split(':')[1])
      algos[algo_id]['quantity'] = quantity
      algos[algo_id]['orders'] = {}

  for _line in log_lines:
    if 'order' in _line and 'unconfirmed' in _line:
      tokens = _line.strip()[1:-1].split(',')
      _algo_id = tokens[6]
      _order_id = tokens[1]

      for __line in log_lines:
        if 'order' in __line and 'new' in __line and 'filled' not in __line:
          tokens = __line.strip()[1:-1].split(',')
          __order_id = tokens[1]
          if __order_id != _order_id: continue

          fix_msg = get_fix_msg('D', __order_id)
          _quantity = parse_fix_field(fix_msg, str(38))
          algos[_algo_id]['orders'][_order_id] = {'quantity': float(_quantity)}

  for key, val in algos.items():
    algo_id = key
    orders = val['orders']
    quantity = val['quantity']
    fix_quantity = 0

    for _key, _val in orders.items():
      fix_quantity += _val['quantity']

    if quantity != fix_quantity:
      print('{}: NOK'.format(algo_id))
    else:
      print('{}: OK'.format(algo_id))

  print(algos)
