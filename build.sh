#!/bin/bash
# WinTune APK Build Script
# Builds the APK with all 6 enhancement features

set -e

echo "🏗️  Building WinTune APK..."
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
    echo "⚠️  Warning: index.html not found in assets, creating placeholder..."
    # If PWA-WEBVIEW-IMPLEMENTATION.md exists, extract the HTML from it
    if [ -f "../PWA-WEBVIEW-IMPLEMENTATION.md" ]; then
        echo "Found PWA-WEBVIEW-IMPLEMENTATION.md, HTML should be in assets/index.html"
    fi
fi

# Build the APK
echo "🔨 Compiling APK..."
cd app
./gradlew assembleRelease

echo ""
echo "✅ Build complete!"
echo "📦 APK location: app/build/outputs/apk/release/app-release.apk"

# Check if APK exists and show size
if [ -f "build/outputs/apk/release/app-release.apk" ]; then
    APK_SIZE=$(du -h "build/outputs/apk/release/app-release.apk" | cut -f1)
    echo "📊 APK size: $APK_SIZE"
    
    echo ""
    echo "🚀 To install on device:"
    echo "   adb install build/outputs/apk/release/app-release.apk"
    echo ""
    echo "💡 First-time setup:"
    echo "   1. Install Termux from F-Droid"
    echo "   2. Open APK and grant permissions"
    echo "   3. Tap 'Start WinTune' when prompted"
fi