@echo off

:: Takes the MSI Name, the folder to bundle as parameters and the Wix config path and the Wix config name without the extension
:: The last parameter is only needed because I don't know how to extract the file name from the path
:: Ex.
:: cmd> call create_msi.bat Application /full/path/to/app/dir/with/exe/ /path/to/app.wxs app

setlocal
set PATH=C:\Program Files (x86)\WiX Toolset v3.14\bin;%PATH%
set msiName=%1
set BuildDir=%2
set WxsFile=%3
set WxsName=%4

:: -nologo - supress heat logo output
:: -suid   - supress uuid for files, directories and components
:: -ag     - Add guids
:: -cd     - Component group name (used in EDMS.wxs)
:: -dr     - We are creating INSTALLDIR
:: -var    - Required to use proper path
:: -out    - Output file (used by candle.exe below)
echo %~dp0fromHeat.wxs
echo %BuildDir%
heat dir "%BuildDir%" -nologo -suid -ag -sfrag -srd -cg FromHeat -dr INSTALLDIR -var var.MyDir -out "%~dp0fromHeat.wxs"
if errorlevel 1 exit 1

:: -out output file (used by light.exe below)
candle -dMyDir="%BuildDir%" "%WxsFile%" "%~dp0fromHeat.wxs" -out %~dp0
::if errorlevel 1 exit 1

light %~dp0%WxsName%.wixobj %~dp0fromHeat.wixobj -o "%~dp0%msiName%"
::if errorlevel 1 exit 1
