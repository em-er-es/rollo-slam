#!/bin/bash
CDATE=$(date '+%d%m%y--%H%M%S')

mkdir -p "$CDATE/raw" "$CDATE/norm" "$CDATE/cal"
mv frame* "$CDATE/raw"
mv norm/frame* "$CDATE/norm"
#ln -sf "$CDATE/raw" latest
rm latest
ln -sv "$CDATE" latest
echo Done
