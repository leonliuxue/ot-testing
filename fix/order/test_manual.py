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


def get_fix_msg(msg_type, order_id):
  # New order single
  # msg_type = 'D'
  # All FIX message for new ordersA
  cmd = '''tail -10000 {} | awk '/35={}/ && /11={}/' '''.format(
      FIX_LOG_FILE, msg_type, order_id)
  out, err = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE).communicate()

  return out


def parse_fix_field(msg, field_no):
  field_val_pairs = {}

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

  for _line in log_lines:
    if 'order' in _line and 'unconfirmed' in _line:
      tokens = _line.strip()[1:-1].split(',')
      _order_id = tokens[1]
      _quantity = float(tokens[10])

      for __line in log_lines:
        if 'order' in __line and 'new' in __line and 'filled' not in __line:
          tokens = __line.strip()[1:-1].split(',')
          __order_id = tokens[1]

          if __order_id != _order_id: continue

          fix_msg = get_fix_msg('D', __order_id)
          __quantity = float(parse_fix_field(fix_msg, str(38)))

          #print([__quantity, _quantity])
          if __quantity != _quantity:
            print('{}: NOK'.format(_order_id))
          else:
            print('{}: OK'.format(_order_id))
