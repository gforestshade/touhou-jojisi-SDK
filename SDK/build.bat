@echo off

rem VS2015�̏ꍇ
call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\Tools\VsDevCmd.bat"

nmake Final_Release
if not "%ERRORLEVEL%"  == "0" (
   echo "compile failed."
   pause
   exit
)
copy /Y Final_Release\CvGameCoreDLL.dll ..\Assets

pause

