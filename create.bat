@echo off
python tools\addChecksum.py < IsraelList.txt > IsraelList2.txt
python tools\validateChecksum.py < IsraelList2.txt
IF ERRORLEVEL 1 GOTO errorHandling
move /y IsraelList2.txt IsraelList.txt
exit
:errorHandling
echo Somthing went wrong
pause