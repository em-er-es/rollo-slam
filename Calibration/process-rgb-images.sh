#!/bin/bash
sh store-rgb-images.sh
CDIR="$(pwd)"
rm latest
ln -sv latest-rgb latest
ls -al latest-rgb
cd latest-rgb && cd raw
sxiv "$CDIR/latest-rgb/raw/"* &
