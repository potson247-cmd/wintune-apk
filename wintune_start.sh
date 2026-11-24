#!/data/data/com.termux/files/usr/bin/bash
# WinTune Android Launcher Script
# Enhancement Features:
# 1. Auto-download folder: Sets WINTUNE_DIR env var to ~/storage/downloads/wintune
# 2. Notifications: Can integrate with Termux:api for desktop notifications
# 3. Dark/Light mode: Not applicable (served via WebView)
# 4. Offline caching: Downloads available in Android download folder
# 5. Multi-language: Python script handles JSON locale files
# 6. Backup & sync: Files in ~/storage/downloads are backed up by Android

# Set working directory
cd ~/wintune || mkdir -p ~/wintune && cd ~/wintune

# Android storage setup (Android 11+)
if [ -d "/storage/downloads" ]; then
    export WIN_TUNE_DIR="/storage/downloads/wintune"
else
    export WIN_TUNE_DIR="$HOME/wintune"
fi

# Create download directory if not exists
mkdir -p "$WIN_TUNE_DIR"

# Install required packages if not present
pkg install -y python ffmpeg yt-dlp curl > /dev/null 2>&1

# Export PATH for Android binaries
export PATH=$PATH:/data/data/com.termux/files/usr/bin

# Download Python script if not exists or outdated
if [ ! -f wintune_android.py ] || [ wintune_android.py -ot "$(date -d '1 day ago' +%s)" ]; then
    echo "Updating WinTune Android version..."
    curl -sL https://raw.githubusercontent.com/frikkieshagger/wintune/main/wintune_android.py -o wintune_android.py
fi

# Download settings.json if not exists
if [ ! -f settings.json ]; then
    echo '{"mp3_dir": "'"$WIN_TUNE_DIR"'", "quality": "0", "embed_thumb": true, "normalize": true}' > settings.json
fi

# Create settings directory
mkdir -p "$WIN_TUNE_DIR/.wintune"

# Export locale for multi-language support
export LANG=$(termux-get-locale 2>/dev/null || echo "en")

# Start WinTune server
echo "Starting WinTune MP3 Downloader..."
echo "Download directory: $WIN_TUNE_DIR"
python wintune_android.py &

# Wait for server to start
sleep 2

# Test connection
if curl -s http://127.0.0.1:8000/version > /dev/null; then
    echo "WinTune server started successfully!"
    echo "Server running at http://127.0.0.1:8000"
    if command -v termux-notification &> /dev/null; then
        termux-notification --title "WinTune" --content "Server started" --priority high
    fi
else
    echo "Failed to start WinTune server"
fi

# Keep terminal open
echo "Press Ctrl+C to stop the server"
wait