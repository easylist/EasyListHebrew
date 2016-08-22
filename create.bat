@echo off
cd %~p0
python tools\addChecksum.py < EasyListHebrew.txt > TempList.txt
python tools\validateChecksum.py < TempList.txt
IF ERRORLEVEL 1 GOTO errorHandling
move /y TempList.txt EasyListHebrew.txt
exit
:errorHandling
echo Something Went Wrong!
pause