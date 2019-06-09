# Methodology
- Send order message to OpenTrade via Python WebSocket. Once OT recieved the request, it will generate the FIX message and send to FIX Simulation Server. The server will simulate the order execution and send back FIX message accordingly to OT. 
- OT will record all FIX communication messages. Check Quickfix FIX message logs to test the correctness.

# Run Test Case
Replace input argument to different test cases
`
python place_orders.py manual_orders.yml --> Wait until all test cases are executed. It will take several minutes depends on the order execution.
python test_fix_orders.py manual_orders.yml
`

# FIX Message Test
## Place New Order
### Manual Order
#### Market Order

#### Limit Order

#### Potential Bugs
1. Test case 14: for GTD, FIX 59 should be 6 but not 0
2. Test case 23: order type is limit, FIX 40 should be 2 but not 1
3. 'teminated' should be 'terminated'

### Algo Order
#### TWAP

## Cancel Order
