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


def get_fix_msg(msg_type, order_id):
  # New order single
  # msg_type = 'D'
  # All FIX message for new ordersA
  cmd = '''tail -10000 {} | awk '/35={}/ && /11={}/' '''.format(FIX_LOG_FILE, msg_type, order_id)
  out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()

  return out

def get_fix_msg1(field_pairs):
      # New order single
  # msg_type = 'D'
  # All FIX message for new ordersA
  cs = []
  for field in field_pairs:
    c = '/{}={}/'.format(field[0], field[1])
    cs.append(c)
  css = '&&'.join(cs)
  #print(css)

  #cmd = '''tail -10000 {} | awk '/35={}/ && /11={}/' '''.format(FIX_LOG_FILE, msg_type, order_id)
  cmd = '''tail -10000 {} | awk '{}' '''.format(FIX_LOG_FILE, css)
  #print(cmd)
  out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()

  return out.strip()


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
      tokens  = line.strip()[1:-1].split(',')
      algo_id = tokens[2]
      exec_tm = tokens[3]
      algos[algo_id] = {'new_orders':{}, 'filled_orders':{}, 'cancelled_orders':{}}
      #algos[algo_id]['orders'] = {}
      #algos[algo_id]['cancelled_orders'] = {}
      quantity = 0
      m = re.search(r'qty\\(.+?),', line)
      if m:
        quantity = float(m.group(1).split(':')[1])
      algos[algo_id]['quantity'] = quantity
      m = re.search(r'Aggression\\(.+?),', line)
      aggression = ''
      if m:
        aggression = m.group(1).split(':')[1][2:-2]
      algos[algo_id]['aggression'] = aggression
    
  #print(algos)
  #exit()
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
          _order_type = parse_fix_field(fix_msg, '40')
          algos[_algo_id]['orders'][_order_id] = {'quantity': float(_quantity), 'order_type': _order_type}

      for __line in log_lines:
        if 'order' in __line and 'cancelled' in __line:
          tokens = __line.strip()[1:-1].split(',')
          __orig_order_id = tokens[1]
          if __order_id != _order_id: continue
          fix_msg = get_fix_msg1([('35','F'), ('41',__orig_order_id)])
          _quantity = parse_fix_field(fix_msg, str(38))
          _order_type = parse_fix_field(fix_msg, '40')
          algos[_algo_id]['cancelled_orders'][_order_id] = {'quantity': float(_quantity), 'order_type': _order_type}
  

  for key, val in algos.items():
    algo_id = key
    orders = val['orders']
    cancelled_orders = val['cancelled_orders']
    quantity = val['quantity']
    aggression = val['aggression']
    fix_quantity = 0
    for _key, _val in orders.items():
      fix_quantity += _val['quantity']
      order_type = _val['order_type']
      if aggression == 'Highest' and TYPE_DICT['market'] != order_type:
        print('{}: NOK. Expacted order type: {}. Real order type: {}'.format(_key, order_type, _order_type))
        continue
    if quantity != fix_quantity:
      print('{}: NOK'.format(algo_id))
      continue
    #else:
    #  print('{}: OK'.format(algo_id))

    if len(cancelled_orders) != 0:
        if len(orders):
            pass

  print(algos)
