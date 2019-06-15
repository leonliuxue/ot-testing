#!/usr/bin/env python2

import mmap
import sys
import struct
import datetime

# order side
kBuy = '1'
kSell = '2'
kShort = '5'

# order type
kMarket = '1'
kLimit = '2'
kStop = '3'
kStopLimit = '4'
kOTC = 'o'

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

kExecTypes = {
    kNew: 'kNew',
    kPartiallyFilled: 'kPartiallyFilled',
    kFilled: 'kFilled',
    kDoneForDay: 'kDoneForDay',
    kCanceled: 'kCanceled',
    kReplaced: 'kReplaced',
    kPendingCancel: 'kPendingCancel',
    kStopped: 'kStopped',
    kRejected: 'kRejected',
    kSuspended: 'kSuspended',
    kPendingNew: 'kPendingNew',
    kCalculated: 'kCalculated',
    kExpired: 'kExpired',
    kAcceptedForBidding: 'kAcceptedForBidding',
    kPendingReplace: 'kPendingReplace',
    kRiskRejected: 'kRiskRejected',
    kUnconfirmedNew: 'kUnconfirmedNew',
    kUnconfirmedCancel: 'kUnconfirmedCancel',
    kUnconfirmedReplace: 'kUnconfirmedReplace',
    kCancelRejected: 'kCancelRejected',
}

# tif
kDay = '0'
kGoodTillCancel = '1'  # GTC
kAtTheOpening = '2'  # OPG
kImmediateOrCancel = '3'  # IOC
kFillOrKill = '4'  # FOK
kGoodTillCrossing = '5'  # GTX
kGoodTillDate = '6'

# exec_trans_type
kTransNew = '0'
kTransCancel = '1'
kTransCorrect = '2'
kTransStatus = '3'


def parse(fn, callback):
  with open(fn, 'r+b') as f:
    # memory-map the file, size 0 means whole file
    mm = mmap.mmap(f.fileno(), 0)
    offset = 0
    while offset + 6 < len(mm):
      seq = struct.unpack('I', mm[offset:offset + 4])[0]
      offset += 4
      n = struct.unpack('H', mm[offset:offset + 2])[0]
      offset += 2
      sub_account_id = struct.unpack('H', mm[offset:offset + 2])[0]
      offset += 2
      exec_type = mm[offset]
      offset += 1
      body = mm[offset:offset + n]
      offset += n + 2  # body + '\0' + '\n'
      fds = body.split()
      if exec_type == kNew:
        id, tm, order_id = fds
        callback(exec_type, id, tm, order_id)
      elif exec_type == kPartiallyFilled or exec_type == kFilled:
        id, tm, last_shares, last_px, exec_trans_type, exec_id = fds
        callback(exec_type, id, tm, last_shares, last_px, exec_trans_type, exec_id)
      elif exec_type == kUnconfirmedNew:
        id, tm, algo_id, qty, price, stop_price, side, type, tif, sec_id, user_id, broker_account_id = fds
        callback(exec_type, id, tm, algo_id, qty, price, stop_price, side, type, tif, sec_id, user_id,
                 broker_account_id)
      elif exec_type == kUnconfirmedCancel:
        id, tm, orig_id = fds
        callback(exec_type, id, tm, orig_id)
      elif exec_type == kRiskRejected:
        id = fds[0]
        text = ' '.join(fds[1])
        callback(exec_type, id, None, text)
      else:
        id, tm = fds[:2]
        text = '.'.join(fds[2:])
        callback(exec_type, id, tm, text)
    assert (offset == len(mm))

  return confirmations


def print_confirmation(*args):
  exec_type = kExecTypes[args[0]]
  id = args[1]
  tm = args[2]
  tm = datetime.datetime.fromtimestamp(float(tm) / 1e6) if tm else ''
  args = (exec_type, id, str(tm)) + args[3:]
  print(args)


confirmations = []


def add_confirmation(*args):
  exec_type = kExecTypes[args[0]]
  id = args[1]
  tm = args[2]
  tm = datetime.datetime.fromtimestamp(float(tm) / 1e6) if tm else ''
  args = (exec_type, id, str(tm)) + args[3:]
  confirmations.append(args)


if __name__ == '__main__':
  parse(sys.argv[1], print_confirmation)
