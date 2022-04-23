#!/bin/bash
tmpList=$(mktemp)
python3 tools/addChecksum.py EasyListHebrew.txt $tmpList
python3 tools/validateChecksum.py $tmpList
if [ $? == 0 ] ; then
  mv -f $tmpList EasyListHebrew.txt
else
  echo 'something went wrong'
fi
python3 genhosts.py EasyListHebrew.txt
