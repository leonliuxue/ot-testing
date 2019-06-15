#!/usr/bin/env python
import sys
from parse_confirmation import parse, print_confirmation, add_confirmation

if __name__ == '__main__':
  if len(sys.argv) == 1:
    print('Error. Order log file should be input argument.')
    exit()

  fn = sys.argv[1]

  log = parse(sys.argv[1], add_confirmation)

  print(log)

  orders = {}
  for line in log:
      if line[0] == 'kPendingNew':
          orders[line[1]] = {':'}
