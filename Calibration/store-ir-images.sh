#!/bin/bash
CDATE=$(date '+%d%m%y--%H%M%S')

mkdir -p "ir-$CDATE/raw" "ir-$CDATE/norm" "ir-$CDATE/cal"
mv frame* "ir-$CDATE/raw"
mv norm/frame* "ir-$CDATE/norm"
#ln -sf "ir-$CDATE/raw" latest
rm latest-ir
ln -sv "ir-$CDATE" latest-ir
echo Done
