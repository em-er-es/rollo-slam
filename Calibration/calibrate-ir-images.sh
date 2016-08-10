#!/bin/bash
python camera-calibration.py -sr3 -sp "latest-ir/cal" -l results.log -ss 48 -ps 7 5 -cr 1280 1024 "latest-ir/raw/"*
echo Done
