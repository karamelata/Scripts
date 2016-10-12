@echo off

for /F "tokens=2" %%i in ('date /t') do set mydate=%%i
set mytime=%time%
echo Current time is %mydate%:%mytime%
echo Copying files...

rem =================================================================================================================
set localData=C:\Data
set extHDData=E:\Data

set logPath=C:\Data\Logs\InternalHDD
set logFileName=%logPath%\%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set maxLogAge=365
rem =================================================================================================================
echo Logging progress in %logFileName%

IF NOT EXIST "%localData%" GOTO localDataNF
IF NOT EXIST "%extHDData%" GOTO intHDDataNF
IF NOT EXIST "%logPath%" GOTO logPathNF

rem | COPY FILES TO SECONDARY HDD |
robocopy %localData% %extHDData% *.* /MIR /XA:SH /W:0 /R:1 /REG /TEE /NP > %logFileName%

rem | COPY LOG FILE ONTO BACKUP DRIVES |
robocopy %logPath% E:\Data\Logs\InternalHDD  /MIR /W:0 /R:1 /REG /TEE
rem | DELETE ANY LOG FILES OLDER THAN 7 DAYS |
forfiles /P "%logPath%" /S /M *.log /D -%maxLogAge% /C "cmd /c del @PATH"

echo Copying and logging complete!
GOTO:EOF

:localDataNF
echo  
echo Unable to find path %localData%
pause
GOTO:EOF
:intHDDataNF
echo  
echo Unable to find path %extHDData%
pause
GOTO:EOF
:logPathNF
echo  
echo Unable to find path %logPath%
pause
GOTO:EOF
