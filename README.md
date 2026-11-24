# WinTune Android APK Implementation

This directory contains the complete Android APK implementation with all 6 enhancement features.

## 📱 Enhancement Features

| # | Feature | File | Description |
|---|---------|------|-------------|
| 1️⃣ | Auto-download Folder | `MainActivity.java`, `wintune_android.py` | Downloads saved to `Downloads/wintune/` |
| 2️⃣ | Notifications | `DownloadService.java` | Foreground service with progress tracking |
| 3️⃣ | Dark/Light Mode | `assets/index.html` | PWA with theme toggle |
| 4️⃣ | Offline Caching | `MainActivity.java` | WebView cache enabled |
| 5️⃣ | Multi-language | `assets/index.html` | English, Spanish, French support |
| 6️⃣ | Backup & Sync | `DownloadService.java` | Files sync with Android backup |

## 📁 Project Structure

```
android_apk/
├── app/
│   ├── src/main/java/com/wintune/
│   │   ├── MainActivity.java      # WebView wrapper + Termux integration
│   │   └── DownloadService.java   # Background download service
│   ├── src/main/assets/
│   │   ├── index.html             # PWA with all features
│   │   ├── wintune_android.py     # Android backend (no Windows .exe)
│   │   └── settings.json          # Default settings
│   ├── src/main/res/
│   │   ├── values/
│   │   │   ├── themes.xml         # App theme
│   │   │   ├── colors.xml         # Color palette
│   │   │   └── strings.xml        # App strings
│   │   ├── values-night/          # Dark theme colors
│   │   └── layout/
│   │       └── activity_main.xml  # Main layout
│   ├── src/main/AndroidManifest.xml
│   ├── app/build.gradle
│   ├── proguard-rules.pro
│   └── APK-QUICK-START.md
├── build.gradle                    # Project-level Gradle
├── settings.gradle                 # Project settings
├── build.sh                        # Build script
└── README.md                       # This file
```

## 🔨 Build Instructions

### Prerequisites
- Android Studio
- Java JDK 11+
- Android SDK

### Build Commands
```bash
# Navigate to project
cd android_apk

# Build release APK
./gradlew assembleRelease

# APK output location
app/build/outputs/apk/release/app-release.apk
```

### Quick Build Script
```bash
chmod +x build.sh
./build.sh
```

## 📦 Installation

### Option 1: Via ADB
```bash
adb install app/build/outputs/apk/release/app-release.apk
```

### Option 2: Direct Download
1. Build the APK
2. Copy `app-release.apk` to your Android device
3. Open file manager and tap the APK
4. Grant storage permissions
5. Install

### First-Time Setup
1. Install Termux from [F-Droid](https://f-droid.org/packages/com.termux/)
2. Open WinTune APK
3. Tap "Start WinTune" when prompted
4. Grant storage permissions in Termux: `termux-setup-storage`

## 🚀 Usage

1. Open WinTune app on Android
2. Tap "Start WinTune" to launch Termux backend
3. Web UI opens automatically in the app
4. Paste YouTube/Spotify URL
5. Click Download
6. MP3s saved to `Downloads/wintune/`

## 🔧 Configuration

### Settings File
Location: `~/.termux/wintune/settings.json` or `~/wintune/settings.json`

```json
{
    "mp3_dir": "/storage/downloads/wintune",
    "quality": "0",
    "embed_thumb": true,
    "normalize": true
}
```

### Quality Options
- `"0"` - Best (default)
- `"128K"` - 128 kbps
- `"192K"` - 192 kbps
- `"320K"` - 320 kbps

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Termux not found" | Install from F-Droid |
| "Server won't start" | Run `termux-setup-storage` |
| "Permission denied" | Grant storage permission |
| "Port already in use" | `pkill -f wintune_android.py` |
| "Downloads failed" | Check `ffmpeg` and `yt-dlp` installed |

## 📊 Technical Details

### Windows .exe Replacement
The original `mp3_downloader.py` uses Windows-specific binaries:
- `yt-dlp.exe` → Python package `yt_dlp`
- `ffmpeg.exe` → Termux package `ffmpeg`
- `picker.exe` → Android storage permissions

### API Endpoints
All endpoints work the same as the web version:
- `GET /` - Web UI
- `GET /files` - List downloaded files
- `GET /dir` - Get download directory
- `GET /settings` - Get settings
- `POST /download` - Start download
- `POST /batch` - Start batch download
- `GET /status/{id}` - Get download status

## 📚 Related Files

- `APK-QUICK-START.md` - Quick reference guide
- `README.md` (parent) - Main project README
- `TERMXUS-ANDROID-SETUP.md` - Full Termux setup guide
- `PWA-WEBVIEW-IMPLEMENTATION.md` - PWA wrapper details

## 📄 License

MIT License - see main project for details.