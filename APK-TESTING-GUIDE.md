# WinTune APK Testing Guide

## 📱 INSTALL ON ANDROID DEVICE

### Option 1: Via ADB (Recommended for Development)

**Prerequisites:**
- Android phone with Developer Options enabled
- USB cable or wireless debugging
- ADB installed on your computer

**Steps:**
```bash
# 1. Connect phone via USB
adb devices

# 2. Install APK
adb install app/build/outputs/apk/release/app-release.apk

# 3. Grant storage permissions
adb shell pm grant com.wintune android.permission.WRITE_EXTERNAL_STORAGE
adb shell pm grant com.wintune android.permission.READ_EXTERNAL_STORAGE
```

### Option 2: Direct Download Method

**Steps:**
1. Build the APK on your computer
2. Transfer to phone via:
   - USB file transfer
   - Email to yourself
   - Cloud storage (Google Drive, Dropbox)
   - WhatsApp/Telegram
3. On phone: Open file manager → tap APK → Install
4. Enable "Install from unknown sources" if prompted

### Option 3: Push to Phone via ADB

```bash
# Push APK to phone's Downloads folder
adb push app/build/outputs/apk/release/app-release.apk /sdcard/Download/

# Install using ADB
adb install /sdcard/Download/app-release.apk
```

---

## 🔧 FIRST-TIME SETUP ON PHONE

**If this is your first time:**

1. **Install Termux** from F-Droid: https://f-droid.org/packages/com.termux/

2. **Install WinTune backend in Termux:**
   ```bash
   pkg update && pkg upgrade
   pkg install python ffmpeg yt-dlp curl termux-api -y
   
   mkdir -p ~/wintune
   cd ~/wintune
   
   # Download the backend
   curl -O https://raw.githubusercontent.com/frikkieshagger/wintune/main/wintune_android.py
   
   # Create settings
   echo '{"mp3_dir": "/storage/downloads/wintune", "quality": "0", "embed_thumb": true, "normalize": true}' > settings.json
   
   # Create download directory
   mkdir -p /storage/downloads/wintune
   
   # Grant storage access
   termux-setup-storage
   ```

3. **Start the server** (either in Termux or via APK):
   ```bash
   cd ~/wintune && python wintune_android.py
   ```

---

## 🧪 TESTING PROCEDURE

### Test 1: App Launch
1. Open WinTune APK
2. Grant all permissions when prompted
3. Should see "WinTune MP3 Downloader" title bar
4. PWA UI should load

### Test 2: Server Connection
1. Tap "Start WinTune" button
2. App should:
   - Check if Termux is installed
   - Prompt to install if missing
   - Start the Python backend
   - Show "Connected" status

### Test 3: Download Functionality
1. Go to the main PWA page
2. Enter a YouTube/Spotify URL
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
| **Dark/Light Mode** | Toggle theme | UI changes immediately |
| **Offline Caching** | Load PWA offline | Content still accessible |
| **Multi-language** | Change device language | UI reflects language |
| **Backup & Sync** | Check settings | .sync file created |

---

## 🐛 DEBUGGING

### View App Logs

```bash
# Filter for WinTune logs
adb logcat | grep wintune

# Or more specific
adb logcat | grep -i "mp3\|download\|wintune"
```

### Check Server Logs

```bash
# In Termux, check server output
# Server logs appear in the terminal where it was started
```

### Common Issues & Fixes

| Issue | Log Error | Solution |
|-------|-----------|----------|
| "Termux not found" | `PackageManager.NameNotFoundException` | Install Termux from F-Droid |
| "Server won't start" | Connection refused to 127.0.0.1:8000 | Run `termux-setup-storage` |
| "Permission denied" | `E/PrivacyGuard` | Grant storage permissions in app settings |
| "Port already in use" | `Address already in use` | `pkill -f wintune_android.py` |
| "Downloads failed" | `yt_dlp` errors | Run `pkg install yt-dlp` in Termux |
| APK won't install | "INSTALL_FAILED_..." | Delete existing app data first |

### APK Size Verification

Expected APK size: **5-10 MB** (WebView wrapper approach)

If APK is much larger, something went wrong with the build.

---

## 📊 VERIFICATION CHECKLIST

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

## 📱 DEVICE COMPATIBILITY

**Minimum Requirements:**
- Android 5.0 (API 21) or higher
- Termux app installed
- Storage permissions granted
- Internet connection

**Recommended:**
- Android 10+ for best storage access
- Termux from F-Droid (not Google Play)
- 50MB+ free storage

---

## 🔗 USEFUL COMMANDS

```bash
# Clear app data
adb shell pm clear com.wintune

# Uninstall app
adb uninstall com.wintune

# Force stop app
adb shell am force-stop com.wintune

# Check if app is installed
adb shell pm list packages | grep wintune

# Open app settings
adb shell am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:com.wintune
```

---

## 📞 SUPPORT

If you encounter issues:
1. Check the logs with `adb logcat | grep wintune`
2. Verify Termux installation and packages
3. Check file permissions
4. Try restarting both Termux and the APK
5. Check GitHub Issues: https://github.com/potson247-cmd/wintune/issues