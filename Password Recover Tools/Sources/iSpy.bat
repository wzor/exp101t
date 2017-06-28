@echo off
findstr /R /C:"^  <Password_" C:\Users\%USERNAME%\AppData\Roaming\iSpy\XML\config.xml > temp
for /F "delims=" %%i in (temp) do set r="%%i"
echo Password: %r:~30,-29%
del temp
pause
