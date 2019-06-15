#!/bin/sh

python ./place_orders4.py twap_orders && ./twap_test.py twap_orders;
python ./place_orders4.py twap_orders_cancel && ./twap_test.py twap_orders_cancel;

