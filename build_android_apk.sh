#!/bin/bash
# WinTune Android APK Build Script
# Run from android_apk directory

set -e

echo "🏗️  Building WinTune Android APK..."
echo ""

# Check if we're in the right directory
if [ ! -f "app/build.gradle" ]; then
    echo "❌ Error: Run this script from the android_apk directory"
    exit 1
fi

# Create asset placeholder directories if needed
mkdir -p app/src/main/assets
mkdir -p app/src/main/res/mipmap-hdpi
mkdir -p app/src/main/res/mipmap-mdpi
mkdir -p app/src/main/res/mipmap-xhdpi
mkdir -p app/src/main/res/mipmap-xxhdpi
mkdir -p app/src/main/res/mipmap-xxxhdpi

# Check if index.html exists in assets
if [ ! -f "app/src/main/assets/index.html" ]; then
    echo "⚠️  Warning: index.html not found in assets"
fi

# Check required files
echo "📋 Checking project files..."
FILES=(
    "app/src/main/java/com/wintune/MainActivity.java"
    "app/src/main/java/com/wintune/DownloadService.java"
    "app/src/main/AndroidManifest.xml"
    "app/src/main/assets/wintune_android.py"
    "app/src/main/assets/settings.json"
    "app/src/main/assets/index.html"
)

ALL_FILES_EXIST=true
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing: $file"
        ALL_FILES_EXIST=false
    fi
done

if [ "$ALL_FILES_EXIST" = false ]; then
    echo "❌ Some required files are missing!"
    exit 1
fi

echo "✅ All required files present"
echo ""

# Build the APK
echo "🔨 Compiling APK..."
cd app
./gradlew assembleRelease

echo ""
echo "✅ Build complete!"
if [ -f "build/outputs/apk/release/app-release.apk" ]; then
    APK_SIZE=$(du -h "build/outputs/apk/release/app-release.apk" | cut -f1)
    echo "📦 APK: app/build/outputs/apk/release/app-release.apk"
    echo "📊 Size: $APK_SIZE"
    echo ""
    echo "🚀 To install on device:"
    echo "   adb install build/outputs/apk/release/app-release.apk"
else
    echo "❌ APK not found at expected location"
    exit 1
fi