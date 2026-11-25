@echo off
REM WinTune APK Build Script for Windows
REM Requires: Java 17, Android SDK (or use WSL)

echo 🏗️  Building WinTune APK...
echo.

REM Check if Java is installed
where java >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Java not found!
    echo Install Java 17 from: https://adoptium.net/
    exit /b 1
)

REM Check Java version
java -version 2>&1 | findstr "17" >nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Java 17 required! Current version:
    java -version
    exit /b 1
)

REM Check if Android SDK is installed
if "%ANDROID_HOME%"=="" (
    if "%ANDROID_SDK_ROOT%"=="" (
        echo ⚠️  Warning: ANDROID_HOME not set
        echo    The build may fail if sdkmanager is not in PATH
    )
)

REM Navigate to project directory
cd /d "%~dp0"

REM Create necessary directories
if not exist "app\src\main\assets" mkdir "app\src\main\assets"
if not exist "app\src\main\res\mipmap-hdpi" mkdir "app\src\main\res\mipmap-hdpi"

REM Check if assets exist
if not exist "app\src\main\assets\index.html" (
    echo ⚠️  Warning: index.html not found in assets
)

REM Build APK
echo 🔨 Compiling APK...
set JAVA_HOME=%JAVA_HOME%
gradlew.bat assembleRelease

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ Build complete!
    if exist "app\build\outputs\apk\release\app-release.apk" (
        echo 📦 APK location: app\build\outputs\apk\release\app-release.apk
        for %%A in ("app\build\outputs\apk\release\app-release.apk") do echo 📊 APK size: %%~zA bytes
    )
) else (
    echo.
    echo ❌ Build failed! Check the error messages above.
)

echo.
echo 🚀 To install on device:
echo    adb install app\build\outputs\apk\release\app-release.apk