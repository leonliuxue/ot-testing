#!/bin/bash

for filename in twap_orders*.yml; do
  IFS='.' read -ra tokens<<<"$filename"
  f=${tokens[0]}
  #echo $f
 python place_orders4.py $f && python test_twap3.py $f
done
