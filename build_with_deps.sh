#!/bin/bash
# WinTune APK Build Script with automatic dependency handling
# Works on WSL, Linux, and macOS

set -e

echo "🏗️  Building WinTune APK..."
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    OS="unknown"
fi

echo "🖥️  Detected OS: $OS"

# Function to check/install Java
setup_java() {
    echo "☕ Checking Java..."
    if command -v java &> /dev/null; then
        JAVA_VERSION=$(java -version 2>&1 | head -1 | cut -d'"' -f2 | cut -d'.' -f1)
        if [ "$JAVA_VERSION" -ge 17 ]; then
            echo "✅ Java $JAVA_VERSION found"
            export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
            return 0
        else
            echo "⚠️  Java version $JAVA_VERSION found, need Java 17"
        fi
    fi
    
    echo "📦 Installing Java 17..."
    if [ "$OS" == "linux" ]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y openjdk-17-jdk
            export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
        elif command -v yum &> /dev/null; then
            sudo yum install -y java-17-openjdk-devel
            export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y java-17-openjdk-devel
            export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
        fi
    elif [ "$OS" == "macos" ]; then
        if command -v brew &> /dev/null; then
            brew install openjdk@17
            export JAVA_HOME=$(/usr/libexec/java_home -v 17)
        fi
    fi
}

# Function to setup Android SDK
setup_android_sdk() {
    echo "🤖 Setting up Android SDK..."
    
    if [ -n "$ANDROID_HOME" ]; then
        echo "✅ ANDROID_HOME already set: $ANDROID_HOME"
        return 0
    fi
    
    SDK_DIR="$HOME/Android/Sdk"
    
    if [ -d "$SDK_DIR" ]; then
        export ANDROID_HOME="$SDK_DIR"
        echo "✅ Android SDK found at $SDK_DIR"
        
        # Install platform if needed
        if [ ! -d "$SDK_DIR/platforms/android-34" ]; then
            echo "📦 Installing Android 34 platform..."
            yes | "$SDK_DIR/tools/bin/sdkmanager" "platforms;android-34" "build-tools;34.0.0"
        fi
        return 0
    fi
    
    echo "⚠️  Android SDK not found. Please install Android Studio or SDK command-line tools."
    echo "   Download from: https://developer.android.com/studio/downloads"
    echo "   Or use Android Studio's SDK manager."
    
    # Try to install via cmdline-tools if available
    if [ -f "$HOME/cmdline-tools/bin/sdkmanager" ]; then
        export ANDROID_HOME="$HOME/cmdline-tools"
        yes | "$ANDROID_HOME/bin/sdkmanager" "platforms;android-34" "build-tools;34.0.0"
        return 0
    fi
    
    return 1
}

# Main build process
build_apk() {
    echo ""
    echo "🔨 Building APK..."
    
    # Make gradlew executable
    chmod +x ./gradlew
    
    # Build
    ./gradlew assembleRelease --no-daemon
    
    if [ -f "app/build/outputs/apk/release/app-release.apk" ]; then
        echo ""
        echo "✅ Build successful!"
        APK_SIZE=$(du -h "app/build/outputs/apk/release/app-release.apk" | cut -f1)
        echo "📊 APK size: $APK_SIZE"
        echo "📦 APK location: app/build/outputs/apk/release/app-release.apk"
        echo ""
        echo "🚀 To install on device:"
        echo "   adb install app/build/outputs/apk/release/app-release.apk"
        return 0
    else
        echo ""
        echo "❌ Build failed! APK not found."
        return 1
    fi
}

# Check prerequisites
check_prerequisites() {
    echo "🔍 Checking prerequisites..."
    
    # Check if we're in the right directory
    if [ ! -f "app/build.gradle" ]; then
        echo "❌ Error: Run this script from the android_apk directory"
        exit 1
    fi
    
    # Check Gradle
    if [ ! -f "gradlew" ]; then
        echo "⚠️  Gradle wrapper not found. This may fail."
    fi
}

# Main execution
main() {
    check_prerequisites
    
    # Setup dependencies
    setup_java
    setup_android_sdk
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "⚠️  Some dependencies missing. You may need to set up:"
        echo "   - Java 17: Install OpenJDK 17"
        echo "   - Android SDK: Install Android SDK with build-tools 34.0.0 and platform 34"
        echo ""
        echo "   Alternative: Use build.bat on Windows or run in Android Studio"
    fi
    
    build_apk
}

main "$@"