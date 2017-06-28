@echo off
reg export "HKLM\Software\Wow6432Node\SXR Software\StatWin" dump.reg
for %%i in (ExecStat, SeeStat) do reg delete "HKLM\Software\Wow6432Node\SXR Software\StatWin\%%i" /v "SystemData" /f
"C:\Program Files (x86)\SXR Software\StatWin\SeeStat.exe"
reg import dump.reg
del dump.reg
