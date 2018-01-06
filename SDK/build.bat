rem VS2015�̏ꍇ
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat"
cd %~dp0

nmake Final_Release
copy /Y Final_Release\CvGameCoreDLL.dll ..\Assets
pause
