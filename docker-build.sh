#!/bin/bash
# Build WinTune APK using Docker (for local builds without Android SDK setup)
# Requires Docker to be installed

set -e

echo "🏗️  Building WinTune APK using Docker..."
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    echo "   On Ubuntu/Debian: sudo apt install docker.io"
    echo "   On macOS: Download from https://docker.com"
    exit 1
fi

# Create a temporary build directory
BUILD_DIR=$(mktemp -d)
echo "📁 Using build directory: $BUILD_DIR"

# Copy project files to build directory
cp -r . "$BUILD_DIR/"

# Build using Android SDK Docker image
docker run --rm \
    -v "$BUILD_DIR:/home/build" \
    -v "$PWD/app/build/outputs:/home/build/app/build/outputs" \
    -w /home/build \
    openjdk:17-jdk-slim \
    bash -c "
        apt-get update && apt-get install -y curl unzip
        # Download Android SDK
        mkdir -p /opt/android-sdk
        cd /opt/android-sdk
        curl -o sdk-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
        unzip -q sdk-tools.zip
        rm sdk-tools.zip
        # Accept licenses and install build tools
        yes | /opt/android-sdk/tools/bin/sdkmanager --licenses
        /opt/android-sdk/tools/bin/sdkmanager 'build-tools;34.0.0' 'platforms;android-34'
        # Set environment
        export ANDROID_HOME=/opt/android-sdk
        export PATH=\$PATH:\$ANDROID_HOME/tools:\$ANDROID_HOME/build-tools/34.0.0
        # Build
        chmod +x gradlew
        ./gradlew assembleRelease
    "

echo ""
echo "✅ Build complete!"
if [ -f "app/build/outputs/apk/release/app-release.apk" ]; then
    APK_SIZE=$(du -h "app/build/outputs/apk/release/app-release.apk" | cut -f1)
    echo "📊 APK size: $APK_SIZE"
    echo "📦 APK location: app/build/outputs/apk/release/app-release.apk"
fi