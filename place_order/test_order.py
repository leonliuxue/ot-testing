#!/usr/bin/env python
import os
import subprocess
import yaml

execute_log_file = './execute_log.yml'

if __name__ == '__main__':
  with open(execute_log_file, 'r') as f:
    execute_logs = yaml.safe_load(f)
  
  
  for key, val in execute_logs.items():
      print('{}:{}'.format(key, val))
      test_time = val['test_time']
      
      log_file = '/home/xzzzx/opentrade/store/fix/FIX.4.2-ot-sim.messages.current.log'
      cmd = '''awk -F, '$1 >= "{}" && /35=D/' < {}'''.format(test_time, log_file)
      out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
      print(out)




