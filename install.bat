@ECHO OFF

:: delete script created for any reasons
if exist eff_exec.bat del /q /f eff_exec.bat

:: query python version used for POL GUI
set /p pythonVersion=Enter the Python Version you want to use (ex. 3.8):

:: upgrade pip and install requirements
call py -%pythonVersion% -m pip install --upgrade pip
call py -%pythonVersion% -m pip install -r requirements.txt

:: create exec bat file for efficiency
echo @ECHO OFF >> "eff_exec.bat"
echo pushd %~dp0 >> "eff_exec.bat"
echo call :LOG > output.log >> "eff_exec.bat"
echo exit /B >> "eff_exec.bat"
echo :LOG >> "eff_exec.bat"
echo py -%pythonVersion% effapp.py >> "eff_exec.bat"

:: create shortcut for efficiency
echo [InternetShortcut] > "%UserProfile%\desktop\EFFICIENCY_GUI.url"
echo URL=%~dp0eff_exec.bat >> "%UserProfile%\desktop\EFFICIENCY_GUI.url"
echo IconFile=%~dp0guiFiles\infineon.ico >> "%UserProfile%\desktop\EFFICIENCY_GUI.url"
echo IconIndex=0 >> "%UserProfile%\desktop\EFFICIENCY_GUI.url"
echo HotKey=0 >> "%UserProfile%\desktop\EFFICIENCY_GUI.url"
echo IDList= >> "%UserProfile%\desktop\EFFICIENCY_GUI.url"
