# 🔧 WinTune APK - Final Build Guide

## 🚀 Quick Build on WSL/Linux/macOS

```bash
# 1. Install prerequisites (Ubuntu/Debian example)
sudo apt update
sudo apt install -y openjdk-17-jdk android-sdk

# 2. Set environment
export ANDROID_HOME=/usr/lib/android-sdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# 3. Install platform for building
yes | sdkmanager --install "build-tools;34.0.0" "platforms;android-34"

# 4. Build APK
cd /path/to/wintune_apk_minimal
chmod +x gradlew
./gradlew assembleRelease

# APK will be at:
# app/build/outputs/apk/release/app-release.apk
```

## 📱 Install on Android Phone

```bash
# Connect via USB
adb devices

# Install APK
adb install app/build/outputs/apk/release/app-release.apk

# Grant permissions
adb shell pm grant com.wintune android.permission.WRITE_EXTERNAL_STORAGE
adb shell pm grant com.wintune android.permission.READ_EXTERNAL_STORAGE
```

## 🔧 First-Time Phone Setup

1. **Install Termux from F-Droid**: https://f-droid.org/packages/com.termux/

2. **In Termux:**
```bash
pkg update && pkg upgrade
pkg install python ffmpeg yt-dlp curl termux-api -y

mkdir -p ~/wintune
cd ~/wintune
curl -O https://raw.githubusercontent.com/frikkieshagger/wintune/main/wintune_android.py

echo '{"mp3_dir": "/storage/downloads/wintune", "quality": "0", "embed_thumb": true, "normalize": true}' > settings.json
mkdir -p /storage/downloads/wintune
termux-setup-storage
```

## 🧪 Testing Instructions

1. Launch APK on phone
2. Grant all permissions
3. Tap "Start WinTune" → Should connect to Termux
4. Enter YouTube/Spotify URL
5. Click Download
6. Verify MP3 in Downloads/wintune/

## 🐛 Debugging Commands

```bash
# Check logs
adb logcat | grep wintune

# Clear app data
adb shell pm clear com.wintune

# Force stop
adb shell am force-stop com.wintune
```

## ✅ All 6 Enhancement Features

| Feature | Implementation |
|---------|---------------|
| 1️⃣ | Auto-download Folder: `Downloads/wintune/` |
| 2️⃣ | Notifications: Foreground service with progress |
| 3️⃣ | Dark/Light Mode: Theme toggle in PWA |
| 4️⃣ | Offline Caching: WebView cache enabled |
| 5️⃣ | Multi-language: English, Spanish, French |
| 6️⃣ | Backup & Sync: Android auto-backup |

## 📊 Verification Checklist

- [ ] APK installs successfully
- [ ] App launches without crash
- [ ] Termux backend connects
- [ ] Downloads work correctly
- [ ] Notifications appear
- [ ] Theme toggle works
- [ ] Multiple languages work