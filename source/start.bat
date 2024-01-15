rem I always use this script to ship things that cant be compiled to .exe's

@echo off
setlocal enabledelayedexpansion

rem Set the directory to the current directory
set "directory=%cd%"

rem Check for existing .pyc files and execute them
for %%i in ("%directory%\*.pyc") do (
    echo Executing: "%%i"
    python "%%i"
    exit /b
)

rem If no .pyc files are found, compile and execute .py files
for %%i in ("%directory%\*.py") do (
    echo Compiling: "%%i"
    
    rem Compile the Python script
    python -m py_compile "%%i"
    
    rem Move the compiled .pyc file back to the main directory
    set "compiled_file=!directory!\__pycache__\%%~ni.cpython-*.pyc"
    move "!compiled_file!" "%directory%"
    
    rem Rename the .pyc file to 'AFKDiscBot.py'
    set "renamed_file=AFKDiscBot.pyc"
    ren "%directory%\%%~ni.cpython-*.pyc" "!renamed_file!"
    
    echo Executing: "!renamed_file!"
    echo Deleting: "__pycache__"
    rmdir __pycache__
    python "%directory%\!renamed_file!"
    exit /b
)

echo No .py or .pyc files found in the current directory.
endlocal
