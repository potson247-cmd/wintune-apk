@echo off
REM WinTune Android APK Build Script for Windows
REM Requires Android Studio or Android SDK to be installed

echo ============================================
echo WinTune Android APK Builder
echo ============================================
echo.

REM Check for Android Studio
if not defined ANDROID_HOME (
    echo Checking for Android Studio...
    for %%a in ("C:\Program Files\Android\Android Studio\bin\studio64.exe") do (
        set "ANDROID_HOME=%%~dapa\..\..\..\.."
    )
)

REM Check for SDK in common locations
if not exist "%ANDROID_HOME%\build-tools" (
    for %%d in (
        "%LOCALAPPDATA%\Android\Sdk"
        "%USERPROFILE%\AppData\Local\Android\Sdk"
        "C:\Android\Sdk"
    ) do (
        if exist "%%d\build-tools" (
            set "ANDROID_HOME=%%d"
        )
    )
)

if not defined ANDROID_HOME (
    echo ERROR: Android SDK not found!
    echo.
    echo Please install Android Studio or set ANDROID_HOME environment variable
    echo Download: https://developer.android.com/studio
    echo.
    pause
    exit /b 1
)

echo Android SDK found at: %ANDROID_HOME%
echo.

REM Set environment for Gradle
set ANDROID_SDK_ROOT=%ANDROID_HOME%
set JAVA_HOME=%JAVA_HOME%

REM Check Java
echo Checking Java...
java -version 2>nul
if errorlevel 1 (
    echo ERROR: Java not found!
    echo Please install JDK 11 or add to PATH
    pause
    exit /b 1
)

echo.
echo Building APK...
echo ============================================

cd /d "%~dp0"

REM Build the APK
echo Running Gradle build...
call ./gradlew.bat assembleRelease

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo BUILD SUCCESSFUL!
echo ============================================
echo APK Location:
echo   app\build\outputs\apk\release\app-release.apk
echo.
echo To install on device:
echo   adb install app\build\outputs\apk\release\app-release.apk
echo.
pause