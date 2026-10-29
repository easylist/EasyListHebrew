#!/bin/bash
./fop-linux -n .
./fop-linux -n --add-checksum=EasyListHebrew.txt
python3 .github/scripts/genhosts.py EasyListHebrew.txt
