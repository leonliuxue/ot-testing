#!/usr/bin/env python
import os
import subprocess
import yaml

execute_log_file = './execute_log.yml'


def parse_fix_order_market(fix_msg, val):

  symbol = '55=' + val['symbol']
  acc = '56=' + val['msg'][2].lower()

  side = val['msg'][3]
  if side == 'Sell':
    side = '54=2'
  elif side == 'Buy':
    side = '54=1'

  type = val['msg'][4]
  if type == 'market':
    type = '40=1'

  tif = val['msg'][5]
  if tif == 'Day':
    tif = '59=0'

  quantity = '38=' + str(val['msg'][6])

  #price =  val['msg'][7]

  if symbol in fix_msg and acc in fix_msg and side in fix_msg and type in fix_msg and tif in fix_msg and quantity in fix_msg:
    print('OK')
  else:
    print('NOK')

  print('\n')


if __name__ == '__main__':
  with open(execute_log_file, 'r') as f:
    execute_logs = yaml.safe_load(f)

  for key, val in execute_logs.items():
    print('Test case: {}'.format(key))
    print('WS msg: {}'.format(val))

    test_time = val['test_time']

    log_file = '/home/xzzzx/opentrade/store/fix/FIX.4.2-ot-sim.messages.current.log'
    cmd = '''awk -F, '$1 >= "{}" && /35=D/ && /5={}/' < {}'''.format(
        test_time, val['symbol'], log_file)
    out, err = subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE).communicate()

    print('Fix msg: {}'.format(out.strip()))

    parse_fix_order_market(out, val)
