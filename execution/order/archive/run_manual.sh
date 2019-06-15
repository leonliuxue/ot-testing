#!/bin/sh

python ./place_orders4.py manual_orders && ./manual_test.py manual_orders;
python ./place_orders4.py manual_orders_cancel && ./manual_test.py manual_orders_cancel;
