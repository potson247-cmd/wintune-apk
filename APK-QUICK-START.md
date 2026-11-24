# WinTune APK Quick Start Guide (Updated)

## Overview
Quick reference for building WinTune APK on Android with all 6 enhancement features.

---

## Enhancement Features Implemented

| # | Feature | Status | Description |
|---|---------|--------|-------------|
| 1️⃣ | Auto-download Folder | ✅ Complete | Downloads to Android Downloads/wintune folder |
| 2️⃣ | Notifications | ✅ Complete | Foreground service with download progress |
| 3️⃣ | Dark/Light Mode | ✅ Complete | Theme toggle, respects system preference |
| 4️⃣ | Offline Caching | ✅ Complete | WebView cache enabled, files accessible offline |
| 5️⃣ | Multi-language | ✅ Complete | English, Spanish, French support |
| 6️⃣ | Backup & Sync | ✅ Complete | Android auto-backup integration |

---

## 📱 INSTALL ON ANDROID DEVICE

### Option 1: Manual Install (Simplest)

**Steps:**
1. Install Termux from [F-Droid](https://f-droid.org/packages/com.termux/)
2. Install required packages in Termux:
   ```bash
   pkg update && pkg upgrade
   pkg install python ffmpeg yt-dlp curl termux-api -y
   ```
3. Create WinTune directory:
   ```bash
   mkdir -p ~/wintune
   cd ~/wintune
   curl -O https://raw.githubusercontent.com/frikkieshagger/wintune/main/wintune_android.py
   echo '{"mp3_dir": "/storage/downloads/wintune", "quality": "0", "embed_thumb": true, "normalize": true}' > settings.json
   mkdir -p /storage/downloads/wintune
   ```
4. Setup storage access:
   ```bash
   termux-setup-storage
   ```
5. Start server:
   ```bash
   cd ~/wintune && python wintune_android.py
   ```

### Option 2: APK + Termux (Recommended)

**Steps:**
1. Build/install the APK from `android_apk/` directory
2. Install Termux from F-Droid
3. Open APK → it will check for Termux and guide installation
4. Grant storage permissions
5. Tap "Start WinTune" → launches Termux and starts server

---

## 🔨 BUILD THE APK

### Prerequisites
- Android Studio (for build)
- Java JDK 11+
- Android SDK

### Build Commands
```bash
# Navigate to Android project
cd android_apk

# Build using Gradle
./gradlew assembleRelease

# APK will be at:
app/build/outputs/apk/release/app-release.apk
```

### Alternative: Quick Build Script
```bash
# Run the quick build
./build_apk.sh
```

---

## 📋 POST-INSTALL CHECKLIST

- [ ] Termux installed from F-Droid
- [ ] Required packages: python, ffmpeg, yt-dlp
- [ ] Storage permissions granted (`termux-setup-storage`)
- [ ] Download folder created: `~/storage/downloads/wintune`
- [ ] APK installed and opens correctly
- [ ] Server starts and shows "Connected" status
- [ ] Download functionality works

---

## 🛠️ TROUBLESHOOTING

| Issue | Quick Fix |
|-------|-----------|
| "Termux not found" | Install from F-Droid: `https://f-droid.org/packages/com.termux/` |
| "Server won't start" | Run `termux-setup-storage` first |
| "Permission denied" | Grant Storage permission in settings |
| "Port already in use" | `pkill -f wintune_android.py` |
| "Downloads not working" | Check `ffmpeg` and `yt-dlp` installed: `which ffmpeg` |
| "App crashes on start" | Check logs: `adb logcat \| grep wintune` |

---

## 🔧 SETTINGS

The settings file at `~/wintune/settings.json` supports:

```json
{
    "mp3_dir": "/storage/downloads/wintune",
    "quality": "0",           // 0=Best, 128K, 192K, 320K
    "embed_thumb": true,     // Embed thumbnails in MP3
    "normalize": true        // Normalize to -14 LUFS
}
```

---

## 🗂️ PROJECT STRUCTURE

```
android_apk/
├── app/
│   ├── src/main/java/com/wintune/
│   │   ├── MainActivity.java      # WebView wrapper
│   │   └── DownloadService.java   # Background download service
│   ├── src/main/assets/
│   │   ├── index.html             # PWA with all features
│   │   ├── wintune_android.py     # Android Python backend
│   │   └── settings.json          # Default settings
│   └── src/main/res/
│       └── mipmap-*/             # App icons
├── build.gradle
├── settings.gradle
├── build.sh                       # Quick build script
└── README.md
```

---

## 🌐 LANGUAGE SUPPORT

Multi-language support (Enhancement #5):

| Language | Code | Status |
|----------|------|--------|
| English | en | ✅ Default |
| Spanish | es | ✅ Available |
| French | fr | ✅ Available |

Languages are auto-detected from system locale.

---

## 🔄 BACKUP & SYNC

Enhancement #6 (Backup & Sync):

- Files are saved to Android Downloads folder
- Automatically synced with Google Backup
- Access via Settings → Google → Backup
- History saved to `~/wintune/history.json`

---

## 📦 FILES DOWNLOAD LOCATION

Enhancement #1 (Auto-download folder):

- Default: `/storage/downloads/wintune/`
- Change via settings or environment variable `WIN_TUNE_DIR`
- Files are accessible in Android Downloads app

---

## 📊 NOTIFICATIONS

Enhancement #2 (Notifications):

- Foreground service shows download progress
- Notifications appear in status bar
- Tap to open WinTune PWA

---

## 🎨 THEME SUPPORT

Enhancement #3 (Dark/Light Mode):

- PWA has built-in theme toggle
- Respects system theme setting
- Toggle button in status bar

---

## 💾 OFFLINE ACCESS

Enhancement #4 (Offline Caching):

- WebView cache enabled
- Download history saved
- Files accessible offline
- No network required after initial load

---

## 📖 FURTHER READING

- `TERMXUS-ANDROID-SETUP.md` - Full Termux setup guide
- `README.md` - Project documentation
- `wintune_start.sh` - Termux launcher script