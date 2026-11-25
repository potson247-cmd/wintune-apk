# WinTune APK Build & Test Guide

## 🚀 Quick Build Instructions

### On WSL/Linux/macOS
```bash
# Navigate to project
cd /path/to/wintune_apk_minimal

# Make script executable
chmod +x build_with_deps.sh

# Build APK
./build_with_deps.sh
```

### On Windows
```cmd
# Open Command Prompt as Administrator
cd D:\User\open\wintune_apk_minimal
build.bat
```

### Using Android Studio
1. Open `android_apk` folder in Android Studio
2. Click "Run" or press Shift+F10
3. Select "app" module
4. APK will be built to: `app/build/outputs/apk/release/app-release.apk`

---

## 📱 INSTALL ON ANDROID DEVICE

### Option 1: Via ADB (Recommended)
```bash
# Connect phone via USB
adb devices

# Install APK
adb install app/build/outputs/apk/release/app-release.apk

# Grant permissions
adb shell pm grant com.wintune android.permission.WRITE_EXTERNAL_STORAGE
adb shell pm grant com.wintune android.permission.READ_EXTERNAL_STORAGE
```

### Option 2: Direct Download
1. Build APK on your computer
2. Transfer to phone via USB, email, or cloud storage
3. On phone: Open file manager → tap APK → Install
4. Enable "Install from unknown sources" if prompted

---

## 🔧 FIRST-TIME SETUP ON PHONE

**Install Termux first:**
1. Install Termux from **F-Droid**: https://f-droid.org/packages/com.termux/
2. Open Termux and install dependencies:

```bash
pkg update && pkg upgrade
pkg install python ffmpeg yt-dlp curl termux-api -y

# Create WinTune directory
mkdir -p ~/wintune
cd ~/wintune

# Download backend script
curl -O https://raw.githubusercontent.com/frikkieshagger/wintune/main/wintune_android.py

# Create settings file
echo '{"mp3_dir": "/storage/downloads/wintune", "quality": "0", "embed_thumb": true, "normalize": true}' > settings.json

# Create download directory
mkdir -p /storage/downloads/wintune

# Grant storage access
termux-setup-storage
```

---

## 🧪 Testing Instructions

### Test 1: App Launch
1. Open WinTune APK on your phone
2. Grant all permissions when prompted
3. PWA UI should load with title "WinTune MP3 Downloader"

### Test 2: Server Connection
1. Tap "Start WinTune" button
2. App checks for Termux → if missing, prompts installation
3. If Termux installed, starts Python backend server
4. Should show "Connected" status

### Test 3: Download Functionality
1. Go to homepage
2. Paste YouTube/Spotify URL
3. Click "Download"
4. Verify:
   - Notification appears
   - Progress updates
   - MP3 saved to Downloads/wintune/

### Test 4: All Enhancement Features

| Feature | How to Test | Expected Result |
|---------|-------------|-----------------|
| **Auto-download Folder** | Download a track | File in `Downloads/wintune/` |
| **Notifications** | Start download | Progress notification visible |
| **Dark/Light Mode** | Tap theme toggle | UI changes immediately |
| **Offline Caching** | Load PWA offline | Content still accessible |
| **Multi-language** | Change device language | UI reflects language |
| **Backup & Sync** | Check for .sync file | `.wintune-sync` file created |

---

## 🐛 Debugging Commands

```bash
# View app logs
adb logcat | grep wintune

# More specific logs
adb logcat | grep -i "mp3\|download\|term"

# Clear app data
adb shell pm clear com.wintune

# Force stop app
adb shell am force-stop com.wintune

# Check if app is installed
adb shell pm list packages | grep wintune

# Open app settings
adb shell am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:com.wintune
```

### Common Issues

| Issue | Log Error | Solution |
|-------|-----------|----------|
| "Termux not found" | `PackageManager.NameNotFoundException` | Install Termux from F-Droid |
| "Server won't start" | Connection refused to 127.0.0.1:8000 | Run `termux-setup-storage` |
| "Permission denied" | `E/PrivacyGuard` | Grant storage permissions in app settings |
| "Port already in use" | `Address already in use` | `pkill -f wintune_android.py` |
| "Downloads failed" | `yt_dlp` errors | Run `pkg install yt-dlp` in Termux |
| APK won't install | "INSTALL_FAILED_..." | Delete existing app data first |

---

## 📊 Verification Checklist

After installing and testing:

- [ ] App launches without crashing
- [ ] WebView loads PWA correctly
- [ ] Termux integration works
- [ ] Server starts and connects
- [ ] Download functionality works
- [ ] MP3 files save to correct location
- [ ] Notifications appear during download
- [ ] Theme toggle works
- [ ] Language changes reflected
- [ ] Files are backed up properly

---

## 🔗 Useful Links

- **Termux (F-Droid)**: https://f-droid.org/packages/com.termux/
- **WinTune GitHub**: https://github.com/potson247-cmd/wintune
- **yt-dlp**: https://github.com/yt-dlp/yt-dlp
- **Android SDK**: https://developer.android.com/studio

---

## 📱 Device Requirements

**Minimum:**
- Android 5.0 (API 21) or higher
- Termux app installed
- Storage permissions granted
- Internet connection

**Recommended:**
- Android 10+ for best storage access
- Termux from F-Droid (not Google Play)
- 50MB+ free storage

**APK Size:** 5-10 MB (WebView wrapper)