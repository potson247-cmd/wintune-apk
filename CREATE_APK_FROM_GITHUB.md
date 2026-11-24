# Alternative: Generate APK via GitHub Actions

If you don't have Android SDK locally, you can use GitHub Actions to build the APK.

## Option 1: GitHub Actions (Recommended)

1. Fork this repository
2. The project includes `.github/workflows/build-apk.yml`
3. Push to your fork - APK will be built automatically
4. Download APK from Actions tab

## Option 2: Use Android Build Service

1. Sign up at **[bughd.com](https://bughd.com)** or similar service
2. Upload the `android_apk` folder
3. Request build
4. Download the generated APK

## Option 3: Local Build with SDK

### Install Android SDK Command Line Tools

```bash
# Download command line tools
curl -o cmdtools.zip https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip

# Extract
mkdir cmdline-tools
unzip cmdtools.zip -d cmdline-tools/temp
mkdir cmdline-tools\cmdline-tools
mv cmdline-tools\temp\* cmdline-tools\cmdline-tools\

# Accept licenses
cmdline-tools\cmdline-tools\bin\sdkmanager.bat --licenses

# Install SDK components
cmdline-tools\cmdline-tools\bin\sdkmanager.bat "platform-tools" "build-tools;34.0.0" "platforms;android-34"
```

### Build APK

```cmd
set ANDROID_HOME=path\to\cmdline-tools
cd android_apk
gradlew.bat assembleRelease
```

## Output

The APK will be at: `android_apk/app/build/outputs/apk/release/app-release.apk`

## Size Estimate

- **APK Size**: 5-15 MB
- **Features Included**: All 6 enhancement features