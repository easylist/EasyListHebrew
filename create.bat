@echo off
cd %~p0
python tools\addChecksum.py < EasyListHebrew.txt > IsraelList2.txt
python tools\validateChecksum.py < IsraelList2.txt
IF ERRORLEVEL 1 GOTO errorHandling
move /y IsraelList2.txt EasyListHebrew.txt
exit
:errorHandling
echo Something went wrong
pause