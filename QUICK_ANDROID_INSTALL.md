# Quick Android Installation (No APK Build Required)

If you don't want to build an APK, you can use a simpler approach:

## Option A: PWAs Already Work in Browser

Since the WinTune web interface is a PWA, you can:
1. Open Chrome on Android
2. Go to https://your-server-ip:8000 (when server is running)
3. Tap the "Install" button in Chrome's address bar
4. Gets added to home screen as PWA!

## Option B: Termux Direct Method (Fastest)

1. **Install Termux from F-Droid**
2. **Install dependencies:**
```bash
pkg update && pkg upgrade
pkg install python ffmpeg yt-dlp curl -y
```

3. **Create WinTune directory:**
```bash
mkdir -p ~/wintune
cd ~/wintune
curl -O https://raw.githubusercontent.com/frikkieshagger/wintune/main/wintune_android.py
```

4. **Setup storage:**
```bash
termux-setup-storage
mkdir -p ~/storage/downloads/wintune
```

5. **Run the server:**
```bash
cd ~/wintune
python wintune_android.py
```

6. **Open in browser:**
- Chrome → `http://127.0.0.1:8000`
- Or create a simple launcher script

## Option C: Create APK Without Android Studio

### Using Termux itself (Native Build)

On Android with Termux:
```bash
pkg install git gradle android-tools openjdk -y
git clone https://github.com/your-repo/wintune
cd wintune/android_apk
./gradlew assembleRelease
```

## Option D: Use Existing APK

If you trust pre-built APKs:
1. Check GitHub Releases for pre-built APKs
2. Verify APK signature before installing
3. Enable "Install from unknown sources"

## PWA vs APK Comparison

| Feature | PWA | APK |
|---------|-----|-----|
| Installation | Add to Home Screen | Full app install |
| Offline | Yes (limited) | Yes (full) |
| Notifications | Limited | Full |
| Storage Access | Limited | Full |
| Build Required | No | Yes |

## Recommendation

**For immediate use:** Use Option B (Termux direct)
**For polished app:** Build APK with Option D or use GitHub Actions