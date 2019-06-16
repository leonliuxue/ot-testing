#!/usr/bin/env python
import re
import subprocess
import sys
import json

import yaml
from parse_confirmation import parse, add_confirmation

# exec type
kNew = '0'
kPartiallyFilled = '1'
kFilled = '2'
kDoneForDay = '3'
kCanceled = '4'
kReplaced = '5'
kPendingCancel = '6'
kStopped = '7'
kRejected = '8'
kSuspended = '9'
kPendingNew = 'A'
kCalculated = 'B'
kExpired = 'C'
kAcceptedForBidding = 'D'
kPendingReplace = 'E'
kRiskRejected = 'a'
kUnconfirmedNew = 'b'
kUnconfirmedCancel = 'c'
kUnconfirmedReplace = 'd'
kCancelRejected = 'e'

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

SECURITY_DICT = {
    '12273': 'USDAUD',
    '12295': 'USDSGD',
    '12279': 'USDEUR',
    '12285': 'USDJPY',
    '12278': 'USDCNY',
    '12277': 'USDCNH',
    '12275': 'USDCAD',
    '12280': 'USDGBP',
    '12281': 'USDHKD',
    '12298': 'USDTWD'
}


def get_fix_msg(field_pairs):
  cs = []
  for field in field_pairs:
    c = '/{}={}/'.format(field[0], field[1])
    cs.append(c)
  css = '&&'.join(cs)
  cmd = '''tail -10000 {} | awk '{}' '''.format(FIX_LOG_FILE, css)
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
    log = f.readlines()

  algos = {}
  orders = {}

  for line in log:
    dfs = json.loads(line)
    #print(dfs)
    action = dfs[0]
    if action == 'algo':
      seq_id, algo_id, tm, token, name, status, body = dfs[1:]
      if status == 'new':
        msg = json.loads(body)
        algos[algo_id] = {'msg': msg, 'order_ids': [], 'is_cancelled': False}
      elif status == 'cancel':
        algos[algo_id]['is_cancelled'] = True
    elif action == 'order':
      order_id, tm, seq_no, exec_type = dfs[1:5]
      algo_id = 0
      if exec_type == 'unconfirmed':
        algo_id = dfs[6]
        algos[algo_id]['order_ids'].append(order_id)
      elif exec_type == 'pending':
        orders[order_id] = {'pending': {}}
      elif exec_type == 'new':
        #print(order_id)
        fix_msg = get_fix_msg([('35', 'D'), ('11', order_id)])
        #print(fix_msg)
        qty = float(parse_fix_field(fix_msg, str(38)))
        order_type = parse_fix_field(fix_msg, '40')
        orders[order_id]['new'] = {'qty': qty, 'order_type': order_type}
      elif exec_type == 'filled':
        qty, px = dfs[5:7]
        orders[order_id]['filled'] = {'qty': qty, 'px': px}
    #print(algos)
    #continue
  print(algos)
  print(orders)

  for key, val in algos.items():
    algo_id = key
    msg = val['msg']
    order_ids = val['order_ids']

    expected_qty = msg['Security']['qty']
    real_qty = 0
    for order_id in order_ids:
      real_qty += orders[order_id]['filled']['qty']
    if real_qty != expected_qty:
      print('{},{},{},expected {},real {}'.format('NOK', key, 'qty', expected_qty, real_qty))

    print('{},{}'.format('OK', algo_id))

  f.close()
