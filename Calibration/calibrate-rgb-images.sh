#!/bin/bash
python camera-calibration.py -sr3 -sp "latest-rgb/cal" -l results.log -ss 25 -ps 9 6 -cr 1280 1024 "latest-rgb/raw/"*
echo Done
