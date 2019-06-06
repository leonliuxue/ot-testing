#!/usr/bin/env python
import os
import subprocess
import yaml

TEST_LOG_FILE = 'test_log.yml'

log_file = '/home/xzzzx/opentrade/store/fix/FIX.4.2-ot-sim.messages.current.log'


def parse_fix_order_market(val):
  test_time = val['test_time']
  symbol = val['symbol']
  acc, side, type, tif, quantity = convert_to_fix_fields(val)

  cmd = '''awk -F, '$1 >= "{}" && /35=D/ && /55={}/ && /56={}/ && /54={}/ && /40={}/ && /59={}/ && /38={}/' < {}'''.format(
      test_time, symbol, acc, side, type, tif, quantity, log_file)

  out, err = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE).communicate()
  if out == '':
    print('FIX NOK')
  else:
    #print('FIX msg: {}'.format(out.strip()))
    print('FIX OK')

  print('')


def convert_to_fix_fields(val):
  acc = val['msg'][2].lower()

  side = val['msg'][3]
  if side == 'Sell':
    side = '2'
  elif side == 'Buy':
    side = '1'

  type = val['msg'][4]
  if type == 'market':
    type = '1'

  tif = val['msg'][5].lower()
  if tif == 'day':
    tif = '0'
  elif tif == 'gtc':
    tif = '1'
  elif tif == 'opg':
    tif = '2'
  elif tif == 'ioc':
    tif = '3'
  elif tif == 'fok':
    tif = '4'
  elif tif == 'gtx':
    tif = '5'
  elif tif == 'gtd':
    tif = '6'

  quantity = str(val['msg'][6])

  return [acc, side, type, tif, quantity]


if __name__ == '__main__':

  with open(TEST_LOG_FILE, 'r') as f:
    execute_logs = yaml.safe_load(f)

  for key, val in execute_logs.items():
    print('Test case: {}'.format(key))
    print('WS msg: {}'.format(val))

    if val['type'] == 'market':
      parse_fix_order_market(val)
