@echo off
cd %~p0
fop-win.exe -n .
fop-win.exe -n --add-checksum=EasyListHebrew.txt
python .github\scripts\genhosts.py EasyListHebrew.txt
