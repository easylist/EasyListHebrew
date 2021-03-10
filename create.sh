#!/bin/bash
tmpList=$(mktemp)
python2 tools/addChecksum.py < EasyListHebrew.txt > $tmpList
python2 tools/validateChecksum.py < $tmpList
if [ $? == 0 ] ; then
  mv -f $tmpList EasyListHebrew.txt
else
  echo 'something went wrong'
fi
python2 genhosts.py EasyListHebrew.txt
