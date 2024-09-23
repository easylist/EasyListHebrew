@echo off
cd %~p0
python .github\scripts\addChecksum.py EasyListHebrew.txt TempList.txt
python .github\scripts\validateChecksum.py TempList.txt
IF ERRORLEVEL 1 GOTO errorHandling
move /y TempList.txt EasyListHebrew.txt
python .github\scripts\genhosts.py EasyListHebrew.txt
exit
:errorHandling
echo Something Went Wrong!
pause