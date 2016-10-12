@echo off
for /F "tokens=2" %%i in ('date /t') do set mydate=%%i
set mytime=%time%

set logPath=C:\Data\Logs\Plex
set logFile=%logPath%\%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log

IF NOT EXIST "%logPath%" GOTO logPathNF

echo MEDIA LIBRARY > %logFile% 
echo Date: %mydate% >> %logFile%
echo Time: %mytime% >> %logFile%

echo. >> %logFile%
echo. >> %logFile%

echo =================  MOVIES  ================= >> %logFile%
echo. >> %logFile%
dir C:\Data\Plex\Movies /b >> %logFile%
echo. >> %logFile%


echo =================  TV SHOWS  ================= >> %logFile%
echo. >> %logFile%
dir C:\Data\Plex\"TV Shows" /b >> %logFile%
echo. >> %logFile%


echo =================  MISC VIDEOS  ================= >> %logFile%
echo. >> %logFile%
dir C:\Data\Plex\"Misc Videos" /b >> %logFile%

echo. >> %logFile%
echo =================  END OF FILE  ================= >> %logFile%
GOTO:EOF

:logPathNF
echo  
echo Unable to find path %logPath%
pause
GOTO:EOF