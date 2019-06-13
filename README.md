# OpenTrade
This test project is for OpenTrade: https://github.com/opentradesolutions/opentrade

# Methodology
- Call OpenTrade (OT) API via Python Websocket. e.g. Place new order, check positions/trades, etc.
- Check QuickFix FIX log files to test the correctness of execution. e.g. New order, cancel order, pending order, etc.
- Query OT database to test the correctness of order management. e.g. Positions, Trades, PnL, etc.
- Test other features. e.g. Order depths, market watch, etc.


# Run Test Case
Replace input argument to different test cases.

~~~~
./place_orders.py orders_manual_market --> Wait until all test cases are executed. It will take several minutes depending on the order execution.

./test_manual.py orders_manual.yml
~~~~


# Test Execution Management Features
## Place New Order
- Market Order
- Limit Order
- TWAP Order
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
- Typo in OT. 'teminated' should be 'terminated'
