@echo off

for /F "tokens=2" %%i in ('date /t') do set mydate=%%i
set mytime=%time%
echo Current time is %mydate%:%mytime%
echo Copying files...

rem =================================================================================================================
set localData=C:\Data
set NASData=\\wdmycloud\SVR_Backup\Data

set logPath=C:\Data\Logs\NAS
set logFileName=%logPath%\%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set maxLogAge=365
rem =================================================================================================================
echo Logging progress in %logFileName%

IF NOT EXIST "%localData%" GOTO localDataNF
IF NOT EXIST "%NASData%" GOTO NASDataNF
IF NOT EXIST "%logPath%" GOTO logPathNF

rem | COPY FILES TO NAS |
robocopy %localData% %NASData% *.* /MIR /XA:SH /W:0 /R:1 /REG /FFT /TEE /NP > %logFileName%

rem | COPY LOG FILE ONTO BACKUP DRIVES |
robocopy %logPath% \\wdmycloud\SVR_Backup\Data\Logs\NAS  /MIR /W:0 /R:1 /REG /TEE
rem | DELETE ANY LOG FILES OLDER THAN 7 DAYS |
forfiles /P "%logPath%" /S /M *.log /D -%maxLogAge% /C "cmd /c del @PATH"

echo Copying and logging complete!
GOTO:EOF

:localDataNF
echo  
echo Unable to find path %localData%
pause
GOTO:EOF
:NASDataNF
echo  
echo Unable to find path %NASData%
pause
GOTO:EOF
:logPathNF
echo  
echo Unable to find path %logPath%
pause
GOTO:EOF