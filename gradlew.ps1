# Gradle wrapper launcher for WinTune APK build (PowerShell)
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    $Args
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$GradleHome = $env:ANDROID_SDK_ROOT

# Try to find gradle
$GradleCmd = $null
$PossibleLocations = @(
    "gradle",
    "gradle.bat",
    "$GradleHome\tools\bin\gradle.bat",
    "$env:ANDROID_HOME\tools\bin\gradle.bat"
)

foreach ($loc in $PossibleLocations) {
    if (Get-Command $loc -ErrorAction SilentlyContinue) {
        $GradleCmd = $loc
        break
    }
    if (Test-Path $loc) {
        $GradleCmd = $loc
        break
    }
}

if ($GradleCmd) {
    & $GradleCmd $Args
} else {
    Write-Host "ERROR: Gradle not found. Please install:"
    Write-Host "  1. Android Studio (includes Gradle)"
    Write-Host "  2. Or download from: https://gradle.org/downloads/"
    exit 1
}