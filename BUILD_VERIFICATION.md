# Android APK Build Verification

## 📋 Build Requirements

### Environment Check
- [ ] Android Studio installed
- [ ] Java JDK 11+ installed
- [ ] Android SDK installed
- [ ] ANDROID_HOME environment variable set

### Java Check
```bash
java -version
# Expected output: Java version 11 or higher
```

### Android SDK Check
```bash
sdkmanager --version
# Expected: SDK Manager version
```

---

## 🔨 Build Commands

### Option 1: Using Gradle Wrapper
```bash
cd android_apk
./gradlew assembleRelease
```

### Option 2: Using Build Script
```bash
cd android_apk
chmod +x build_android_apk.sh
./build_android_apk.sh
```

---

## ✅ Verification Checklist

### All Required Files Present

| File | Status | Purpose |
|------|--------|---------|
| `app/src/main/java/com/wintune/MainActivity.java` | ✅ Created | WebView wrapper |
| `app/src/main/java/com/wintune/DownloadService.java` | ✅ Created | Download service |
| `app/src/main/AndroidManifest.xml` | ✅ Created | App manifest |
| `app/src/main/assets/index.html` | ✅ Created | PWA interface |
| `app/src/main/assets/wintune_android.py` | ✅ Created | Android backend |
| `app/src/main/assets/settings.json` | ✅ Created | Settings |
| `app/src/main/res/values/themes.xml` | ✅ Created | App theme |
| `app/src/main/res/values/colors.xml` | ✅ Created | Color palette |
| `app/build.gradle` | ✅ Created | App-level Gradle |
| `build.gradle` (project) | ✅ Created | Project-level Gradle |
| `settings.gradle` | ✅ Created | Gradle settings |

---

## 📊 Expected Output

### APK Size
- **Expected**: 5-15 MB
- **Location**: `android_apk/app/build/outputs/apk/release/app-release.apk`

### Build Reports
- **Build Log**: `app/build/outputs/logs/manifest-placeholders-report.txt`
- **APK Info**: `app/build/outputs/apk/release/output.json`

---

## 🧪 Testing Instructions

### 1. Install APK on Device
```bash
adb install app/build/outputs/apk/release/app-release.apk
```

### 2. Check Installation
```bash
adb shell pm list packages | grep wintune
```

### 3. Launch App
```bash
adb shell am start -n com.wintune/.MainActivity
```

### 4. Check Logs
```bash
adb logcat | grep wintune
```

---

## 🛠️ Troubleshooting

### Build Errors

| Error | Solution |
|-------|----------|
| "Could not find gradle" | Run `gradle wrapper --gradle-version 8.2` |
| "SDK not found" | Set ANDROID_HOME env var |
| "Java version mismatch" | Install Java 11 or set sourceCompatibility |
| "Permission denied" | Check project files are readable |

### Runtime Errors

| Error | Solution |
|-------|----------|
| "Termux not found" | Install from F-Droid |
| "Port 8000 in use" | `pkill -f wintune_android.py` |
| "Download failed" | Check `ffmpeg` and `yt-dlp` in Termux |

---

## 📦 APK Contents Verification

After successful build, verify the APK:

```bash
# List contents
unzip -l app/build/outputs/apk/release/app-release.apk

# Expected assets:
# - index.html
# - wintune_android.py
# - settings.json

# Verify signatures
apksigner verify --verbose app-build/outputs/apk/release/app-release.apk
```

---

## 🎯 Post-Build Actions

### Release Build
1. Sign with release keystore:
```bash
# Generate keystore (if needed)
keytool -genkeypair -v -keystore wintune.keystore -alias wintune -keyalg RSA -keysize 2048 -validity 10000

# Sign APK
jarsigner -keystore wintune.keystore app-release.apk wintune
```

### Distribution
- [ ] Google Play Console upload
- [ ] F-Droid submission
- [ ] GitHub Releases upload

---

## 📝 Build Command Summary

```bash
# 1. Navigate to Android project
cd android_apk

# 2. Build release APK
./gradlew assembleRelease

# 3. Output location
app/build/outputs/apk/release/app-release.apk

# 4. Alternative: Build with script
./build_android_apk.sh
```

---

## ✨ Quick Start After Build

1. Build APK: `./gradlew assembleRelease`
2. Install Termux from F-Droid on device
3. Install APK via ADB: `adb install app/build/outputs/apk/release/app-release.apk`
4. Open APK on device
5. Grant storage permissions
6. Tap "Start WinTune"
7. Use the PWA interface for downloads

Downloads go to: `Downloads/wintune/` on Android