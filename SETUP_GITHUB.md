# GitHub Actions Setup Guide

## 📋 Prerequisites
- GitHub account
- Git installed locally

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create New Repository
1. Go to https://github.com/new
2. Repository name: `wintune`
3. Visibility: Public (for free Actions)
4. Initialize with README: ✅
5. Click "Create repository"

### Step 2: Push Code to GitHub
```bash
# Open terminal in your wintune folder
cd D:\User\open\wintune

# Initialize git (if not already)
git init

# Add all files (excluding local build artifacts)
git add .
git commit -m "WinTune Android APK with all 6 enhancement features"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/wintune.git

# Push to GitHub
git branch -M main
git push -u origin main -f
```

### Step 3: Verify CI/CD is Running
1. Go to: https://github.com/YOUR_USERNAME/wintune/actions
2. Look for "Build APK" workflow
3. Click to view details
4. Wait 2-5 minutes for completion

### Step 4: Download APK
1. In Actions tab, click the completed workflow
2. Scroll down to "Artifacts"
3. Click "wintune-apk" to download
4. Extract if named .zip
5. Install on Android device: `adb install app-release.apk`

## 📱 First Run on Android

### After Installing APK:
1. Open WinTune app
2. Tap "Start WinTune" button
3. Grant storage permissions
4. Enter YouTube/Spotify URL
5. Click Download
6. Check `Downloads/wintune/` folder

---

## 🔧 Troubleshooting

### Workflow Not Running?
- Check if files are in repository
- Verify `.github/workflows/build-apk.yml` exists
- Check Actions tab for any errors

### Build Failed?
- Check workflow logs for errors
- Common issues:
  - Missing files
  - Network timeout
  - Permission issues

### Download APK Not Available?
- Click the workflow run
- Scroll to bottom
- Find "Artifacts" section
- Download wintune-apk

## 📊 Build Expected Results

| Metric | Expected |
|--------|----------|
| APK Size | 8-15 MB |
| Build Time | 2-5 minutes |
| Features | All 6 implemented |
| Min SDK | 21 (Android 5.0+) |
| Target SDK | 34 (Android 14) |

## 🔄 Rebuild APK
Any push to main branch will trigger rebuild:
```bash
git commit --allow-empty -m "Trigger rebuild"
git push
```

## 📚 Documentation
- `BUILD_INSTRUCTIONS.md` - Build details
- `QUICK_ANDROID_INSTALL.md` - Quick PWA alternative
- `APK-QUICK-START.md` - Installation guide
- `README.md` - Project overview