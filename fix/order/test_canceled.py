#!/usr/bin/env python
import subprocess
import sys

import yaml
import re

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

SIDE_DICT = {'buy': '1', 'sell': '2', 'buy minus': '3', 'sell plus': '4', 'sell short': '5', 'sell short exempt': '6'}

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
  cmd = '''tail -10000 {} | awk '/35={}/ && /11={}/' '''.format(FIX_LOG_FILE, msg_type, order_id)
  out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()

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

  for line in log_lines:
    if 'order' in line and 'unconfirmed' in line:
      tokens = line.strip()[1:-1].split(',')
      order_id = tokens[1]
      quantity = float(tokens[10])
      side = SIDE_DICT[tokens[12][1:-1].lower()]
      order_type = TYPE_DICT[tokens[13][1:-1].lower()]
      tif = TIF_DICT[tokens[14][1:-1].lower()]

      for _line in log_lines:
        if 'order' in _line and 'new' in _line and 'filled' not in _line:
          tokens = _line.strip()[1:-1].split(',')
          _order_id = tokens[1]

          if _order_id != order_id: continue

          fix_msg = get_fix_msg('D', _order_id)
          if fix_msg == '':
            print('{},NOK,FIX msg has not found'.format(order_id))
            continue
          _quantity = float(parse_fix_field(fix_msg, '38'))
          if _quantity != quantity:
            print('{}: NOK. Expected side: {}. Actual side: {}'.format(order_id, quantity, _quantity))
            continue
          _side = parse_fix_field(fix_msg, '54')
          if _side != side:
            print('{}: NOK. Expected side: {}. Actual side: {}'.format(order_id, side, _side))
            continue
          _order_type = parse_fix_field(fix_msg, '40')
          if _order_type != order_type:
            print('{}: NOK. Expected side: {}. Actual side: {}'.format(order_id, order_type, _order_type))
            continue
          _tif = parse_fix_field(fix_msg, '59')
          if _tif != tif:
            print('{}: NOK. Expected side: {}. Actual side: {}'.format(order_id, tif, _tif))
            continue

          print('{:3s},{},{:6s}'.format('OK', order_id, 'New'))

      for _line in log_lines:
        if 'order' in _line and 'cancelled' in _line:
          tokens = _line.strip()[1:-1].split(',')
          _order_id = tokens[1]

          if _order_id != order_id: continue

          fix_msg = get_fix_msg('F', _order_id)
          if fix_msg == '':
            print('{:3s},{},{:6s},FIX msg has not found'.format('NOK', order_id, 'Cancel'))
            continue
          _quantity = float(parse_fix_field(fix_msg, '38'))
          if _quantity != quantity:
            print('{}: NOK. Expected side: {}. Actual side: {}'.format(order_id, quantity, _quantity))
            continue
          _side = parse_fix_field(fix_msg, '54')
          if _side != side:
            print('{}: NOK. Expected side: {}. Actual side: {}'.format(order_id, side, _side))
            continue
          _order_type = parse_fix_field(fix_msg, '40')
          if _order_type != order_type:
            print('{}: NOK. Expected side: {}. Actual side: {}'.format(order_id, order_type, _order_type))
            continue
          _tif = parse_fix_field(fix_msg, '59')
          if _tif != tif:
            print('{}: NOK. Expected side: {}. Actual side: {}'.format(order_id, tif, _tif))
            continue

          print('{:3s} ,{},{:6s}'.format('OK', order_id, 'Cancel'))
