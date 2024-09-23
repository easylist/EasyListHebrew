#!/bin/bash
tmpList=$(mktemp)
python3 .github/scripts/addChecksum.py EasyListHebrew.txt $tmpList
python3 .github/scripts/validateChecksum.py $tmpList
if [ $? == 0 ] ; then
  mv -f $tmpList EasyListHebrew.txt
else
  echo 'something went wrong'
fi
python3 .github/scripts/genhosts.py EasyListHebrew.txt
