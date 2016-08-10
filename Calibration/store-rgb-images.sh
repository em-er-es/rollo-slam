#!/bin/bash
CDATE=$(date '+%d%m%y--%H%M%S')

mkdir -p "rgb-$CDATE/raw" "rgb-$CDATE/cal"
mv frame* "rgb-$CDATE/raw"
#ln -sf "rgb-$CDATE/raw" latest
rm latest-rgb
ln -sv "rgb-$CDATE" latest-rgb
echo Done
