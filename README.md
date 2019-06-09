# Methodology
- Call OpenTrade (OT) API via Python Websocket. e.g. Place new order, check positions/trades, etc.
- Check QuickFix FIX log files to test the correctness of execution. e.g. New order, cancel order, pending order, etc.
- Query OT database to test the correctness of order management. e.g. Positions, Trades, PnL, etc.
- Test other features. e.g. Order depths, market watch, etc.


# Run Test Case
Replace input argument to different test cases.

~~~~
python place_orders.py manual_orders.yml --> Wait until all test cases are executed. It will take several minutes depending on the order execution.

python test_fix_orders.py manual_orders.yml
~~~~


# Test Execution Management Features
## Place New Order
- Market Order
- Limit Order
- TWAP
## Cancel Order

# Test Order Management Features
- Pending Orders
- Rejects Orders
- Trades (Filled Orders) 
- Positions
- Order Depths
- Market Watch
- PnL
- Account 

# Bug List (Potential)
1. Test case 14: for GTD, FIX 59 should be 6 but not 0
2. Test case 23: order type is limit, FIX 40 should be 2 but not 1
3. Typo in OT. 'teminated' should be 'terminated'
