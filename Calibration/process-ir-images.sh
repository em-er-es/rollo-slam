#!/bin/bash
python normalize-images.py && sh store-ir-images.sh && rm -r norm
CDIR="$(pwd)"
rm latest
ln -sv latest-ir latest
ls -al latest
cd latest && cd norm
python "$CDIR"/ir-filter-images.py
sxiv "$CDIR/latest/norm/ir/"* &
