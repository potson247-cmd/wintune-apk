# WinTune APK Build Package

## Package Contents

This directory contains everything needed to build the WinTune Android APK.

## Quick Build Instructions

### Windows (Command Line)
```cmd
REM Set Android SDK environment (requires Android Studio installed)
setx ANDROID_HOME "C:\Users\%USERNAME%\AppData\Local\Android\Sdk"
setx JAVA_HOME "C:\Program Files\Android\Android Studio\jre"

REM Build
cd android_apk
gradlew.bat assembleRelease

REM Find APK
echo APK built at: app\build\outputs\apk\release\app-release.apk
```

### Linux/macOS
```bash
# Install dependencies
sudo apt-get install openjdk-11-jdk android-sdk

# Or use Android Studio
# Open Project → Select android_apk/ folder
# Build → Build APK(s)

# Command line build
export ANDROID_HOME=/path/to/android/sdk
./gradlew assembleRelease
```

## If Android SDK is NOT Available

### Option A: Use GitHub Actions (Recommended)
1. Fork this repository: https://github.com/your-username/wintune
2. Push any change to trigger the build
3. Go to "Actions" tab
4. Download "app-release.apk" from the build artifact

### Option B: Use Online Build Service
Visit any of these services and upload the `android_apk` folder:
- https://appetize.io
- https://www.bughd.com
- https://build.phonegap.com

### Option C: Use Genymobile Android Build Service
1. Sign up at https://www.genymotion.com/
2. Upload project
3. Request build

## Package Verification

### Required Files (All Present ✅)

```
📦 android_apk/
├── 📂 app/
│   ├── 📂 src/main/java/com/wintune/
│   │   ├── MainActivity.java      (19.4 KB) - WebView wrapper
│   │   └── DownloadService.java   (5.2 KB) - Background service
│   ├── 📂 src/main/assets/
│   │   ├── index.html             (14.2 KB) - PWA with 6 features
│   │   ├── wintune_android.py     (22.5 KB) - Android backend
│   │   └── settings.json          (139 bytes) - Default settings
│   ├── 📂 src/main/res/
│   │   ├── 📂 values/
│   │   │   ├── themes.xml         (1.1 KB) - App theme
│   │   │   ├── colors.xml         (383 bytes) - Color palette
│   │   │   └── strings.xml        (246 bytes) - App strings
│   │   └── 📂 values-night/
│   │       ├── themes.xml         (972 bytes) - Dark theme
│   │       └── strings.xml        (246 bytes) - Strings
│   │
│   ├── AndroidManifest.xml        (1.7 KB) - App manifest
│   ├── app/build.gradle           (2.2 KB) - App config
│   ├── proguard-rules.pro         (1.3 KB) - ProGuard rules
│   └── 📂 src/main/res/mipmap-*/
│
├── build.gradle                    (586 bytes) - Project config
├── settings.gradle                 (152 bytes) - Gradle settings
├── gradle/
│   └── wrapper/
│       └── gradle-wrapper.properties (203 bytes) - Gradle wrapper config
├── build.bat                       (Windows build script)
├── build.sh                        (Linux build script)
├── build_android_apk.sh            (Quick build script)
├── .github/
│   └── workflows/
│       └── build-apk.yml           (GitHub Actions workflow)
│
├── APK-QUICK-START.md              (Installation guide)
├── BUILD_GUIDE.md                  (Build documentation)
├── BUILD_VERIFICATION.md           (Testing guide)
└── PACKAGING_OPTIONS.md            (Build options)
```

### All Required Permissions Declared

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
```

## APK Features Checklist

| Feature | Implementation |
|---------|---------------|
| Auto-download folder | ✅ `/storage/downloads/wintune/` |
| Notifications | ✅ Foreground service |
| Dark/Light mode | ✅ Theme toggle in PWA |
| Offline caching | ✅ WebView cache |
| Multi-language | ✅ en/es/fr support |
| Backup & sync | ✅ Android backup |

## Next Steps After Build

1. **Test APK**: Install on physical Android device
2. **Install Termux**: From F-Droid on device
3. **Configure**: Set download directory
4. **Use**: Enter URLs and download MP3s

## Support

For issues:
- Check `BUILD_VERIFICATION.md` for troubleshooting
- Open GitHub issue with error logs
- Include Android version and build command output