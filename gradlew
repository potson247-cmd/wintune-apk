#!/usr/bin/env bash
# Gradle wrapper launcher for WinTune APK build
# This script launches the correct Gradle version

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GRADLE_USER_HOME="${GRADLE_USER_HOME:-$HOME/.gradle}"

# Check for Gradle in common locations
GRADLE_CMD=""
for cmd in "gradle" "gradle.bat"; do
    if command -v "$cmd" &> /dev/null; then
        GRADLE_CMD="$cmd"
        break
    fi
done

if [ -n "$GRADLE_CMD" ]; then
    exec "$GRADLE_CMD" "$@"
else
    # Try to find gradle in Android SDK
    if [ -n "$ANDROID_SDK_ROOT" ] && [ -f "$ANDROID_SDK_ROOT/tools/bin/gradle" ]; then
        exec "$ANDROID_SDK_ROOT/tools/bin/gradle" "$@"
    elif [ -n "$ANDROID_HOME" ] && [ -f "$ANDROID_HOME/tools/bin/gradle" ]; then
        exec "$ANDROID_HOME/tools/bin/gradle" "$@"
    else
        echo "ERROR: Gradle not found. Please install:"
        echo "  1. Android Studio (includes Gradle)"
        echo "  2. Or download from: https://gradle.org/downloads/"
        echo "  3. Or install via: sdkmanager"
        exit 1
    fi
fi