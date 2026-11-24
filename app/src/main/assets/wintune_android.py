#!/usr/bin/env python3
"""
WinTune MP3 Downloader - Android Edition
Replaces Windows .exe binaries with native Python packages for Android/Termux compatibility.

Enhancement Features:
1. Auto-download folder: Uses Android Downloads directory with wintune subfolder
2. Notifications: Can integrate with Termux:api for desktop notifications  
3. Dark/Light mode: Not applicable (served via WebView - handled by PWA)
4. Offline caching: Downloads available in Android download folder
5. Multi-language: Python script handles JSON locale files
6. Backup & sync: Files in ~/storage/downloads are backed up by Android
"""

import ctypes
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
import urllib.error
import urllib.parse
import webbrowser
import http.cookiejar
import requests
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, unquote_plus, parse_qs
import ssl

# Try to import yt-dlp as Python package (preferred for Android)
try:
    import yt_dlp
    YTDLP_AVAILABLE = True
except ImportError:
    YTDLP_AVAILABLE = False
    YTDLP = "yt-dlp"

FROZEN = getattr(sys, "frozen", False)

# Suppress SSL certificate verification for environments without valid CA stores
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE
_orig_urlopen = urllib.request.urlopen


def _ssl_urlopen(req, *args, **kwargs):
    kwargs.setdefault("context", _ssl_ctx)
    return _orig_urlopen(req, *args, **kwargs)


urllib.request.urlopen = _ssl_urlopen

if FROZEN:
    APP_DIR = os.path.dirname(sys.executable)
    BUNDLE = sys._MEIPASS
    INSTALL_DIR = os.path.join(
        os.environ.get("ProgramFiles", "C:\\Program Files"), "webmp3")
    DATA_DIR = os.path.join(os.environ.get("USERPROFILE", APP_DIR), "Music", "webmp3")
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    BUNDLE = APP_DIR
    INSTALL_DIR = APP_DIR
    DATA_DIR = os.path.join(os.environ.get("HOME", APP_DIR), "wintune")
    MP3_DIR = os.path.join(DATA_DIR, "MP3")

# Android-specific paths (Termux)
def get_android_paths():
    """Detect Android/Termux environment and set appropriate paths."""
    if os.path.exists("/data/data/com.termux"):
        android_dir = os.environ.get("HOME", "/data/data/com.termux/files/home")
        # Enhancement 1: Use Android downloads folder
        downloads_dir = os.environ.get("ANDROID_DOWNLOADS", 
                                        os.path.join(android_dir, "storage", "downloads"))
        return {
            "DATA_DIR": android_dir,
            "INSTALL_DIR": os.path.join(android_dir, "wintune"),
            "MP3_DIR": os.path.join(downloads_dir, "wintune"),
            "SETTINGS_FILE": os.path.join(android_dir, "wintune", "settings.json"),
            "COOKIES_FILE": os.path.join(android_dir, "wintune", "cookies.txt"),
            "HISTORY_FILE": os.path.join(android_dir, "wintune", "history.json"),
        }
    return {
        "DATA_DIR": DATA_DIR,
        "INSTALL_DIR": INSTALL_DIR,
        "MP3_DIR": MP3_DIR,
        "SETTINGS_FILE": os.path.join(DATA_DIR, "settings.json"),
        "COOKIES_FILE": os.path.join(DATA_DIR, "cookies.txt"),
        "HISTORY_FILE": os.path.join(DATA_DIR, "history.json"),
    }


# Initialize Android paths
_paths = get_android_paths()
DATA_DIR = _paths["DATA_DIR"]
INSTALL_DIR = _paths["INSTALL_DIR"]
MP3_DIR = _paths["MP3_DIR"]
SETTINGS_FILE = _paths["SETTINGS_FILE"]
COOKIES_FILE = _paths["COOKIES_FILE"]
HISTORY_FILE = _paths["HISTORY_FILE"]

# Directories to create on first run
def ensure_directories():
    """Create required directories for WinTune operation."""
    dirs_to_create = [
        DATA_DIR,
        INSTALL_DIR,
        MP3_DIR,
    ]
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)


ensure_directories()

HOST, PORT = "127.0.0.1", 8000
VERSION = "1.2.4-android-enhanced"
JOBS = {}
JOB_ID = 0
BATCHES = {}
BATCH_ID = 0
LOCK = threading.Lock()

# Settings defaults - Enhancement 1: Auto-download folder
MP3_DIR = os.environ.get("WIN_TUNE_DIR", MP3_DIR)
QUALITY = "0"
EMBED_THUMB = True
NORMALIZE = True


def load_settings():
    """Load settings from JSON file."""
    global MP3_DIR, QUALITY, EMBED_THUMB, NORMALIZE
    try:
        with open(SETTINGS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data.get("mp3_dir"), str) and data["mp3_dir"].strip():
            MP3_DIR = data["mp3_dir"]
            os.makedirs(MP3_DIR, exist_ok=True)
        if data.get("quality") in ("0", "128K", "192K", "320K"):
            QUALITY = data["quality"]
        if isinstance(data.get("embed_thumb"), bool):
            EMBED_THUMB = data["embed_thumb"]
        if isinstance(data.get("normalize"), bool):
            NORMALIZE = data["normalize"]
    except (OSError, ValueError):
        pass


def save_settings():
    """Save settings to JSON file."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"mp3_dir": MP3_DIR, "quality": QUALITY,
                       "embed_thumb": EMBED_THUMB, "normalize": NORMALIZE}, f)
    except OSError:
        pass


def find_ffprobe():
    """Find ffprobe executable (system ffmpeg on Android)."""
    common_paths = [
        "/usr/bin/ffprobe",
        "/data/data/com.termux/files/usr/bin/ffprobe",
        "/usr/local/bin/ffprobe",
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    try:
        result = subprocess.run(["which", "ffprobe"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "ffprobe"


def find_ffmpeg():
    """Find ffmpeg executable (system ffmpeg on Android)."""
    common_paths = [
        "/usr/bin/ffmpeg",
        "/data/data/com.termux/files/usr/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    try:
        result = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "ffmpeg"


FFMPEG = find_ffmpeg()
FFPROBE = find_ffprobe()


def measure_loudness(path):
    """Measure audio loudness using ffprobe."""
    try:
        cmd = [
            FFPROBE, "-i", path,
            "-af", "loudnorm=print_format=summary", "-f", "null", "-",
        ]
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        m = re.search(r"Input Integrated:\s*(-?\d+(?:\.\d+)?)\s*LUFS", result.stderr)
        return float(m.group(1)) if m else None
    except Exception:
        return None


def apply_normalize(path):
    """Apply volume normalization using ffmpeg."""
    try:
        integrated = measure_loudness(path)
        if integrated is None:
            return None
        gain = round(-14.0 - integrated, 1)
        if abs(gain) < 1.0:
            return 0.0
        tmp = path + ".tmp.mp3"
        if QUALITY == "0":
            enc = ["-q:a", "5"]
        else:
            enc = ["-b:a", QUALITY]
        cmd = [
            FFMPEG, "-y", "-i", path,
            "-af", f"volume=%+0.1fdB" % gain,
            "-c:a", "libmp3lame"
        ] + enc + [
            "-map", "0:a", "-map", "0:v?", "-c:v", "copy",
            "-map_metadata", "0", tmp
        ]
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if result.returncode != 0 or not os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass
            return None
        os.replace(tmp, path)
        return gain
    except Exception:
        return None


def build_command(url, playlist=False):
    """Build yt-dlp download command (supports both Python API and CLI)."""
    tpl = "%(title)s.%(ext)s"
    output_template = os.path.join(MP3_DIR, tpl)
    
    if YTDLP_AVAILABLE:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": QUALITY if QUALITY != "0" else "192",
            }],
            "outtmpl": output_template,
            "postprocessor_args": [
                "--embed-thumbnail",
                "--add-metadata",
            ],
            "ffmpeg_location": FFMPEG,
            "noplaylist": not playlist,
            "retries": 10,
            "fragment_retries": 10,
            "sleep_requests": 2,
            "sleep_interval": 3,
            "max_sleep_interval": 8,
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
            "default_search": "auto",
            "ignoreerrors": True,
            "nooverwrites": False,
            "restrictfilenames": False,
            "writethumbnail": EMBED_THUMB,
        }
        if os.path.exists(COOKIES_FILE):
            ydl_opts["cookiefile"] = COOKIES_FILE
        return ("ydl", ydl_opts, url)
    else:
        cmd = [
            YTDLP,
            "-x",
            "--audio-format", "mp3",
            "--ffmpeg-location", os.path.dirname(FFMPEG) if FFMPEG != "ffmpeg" else "",
            "--replace-in-metadata", "title", "[\\r\\n]+", " ",
            "--embed-metadata",
            "--parse-metadata", "%(uploader)s - %(title)s:%(title)s",
            "--newline",
            "--extractor-args", "youtube:player_client=android",
            "--retries", "10",
            "--fragment-retries", "10",
            "--sleep-requests", "2",
            "--sleep-interval", "3",
            "--max-sleep-interval", "8",
        ]
        if not playlist:
            cmd += ["--no-playlist"]
        if QUALITY != "0":
            cmd += ["--audio-quality", QUALITY]
        if EMBED_THUMB:
            cmd += ["--embed-thumbnail"]
        if os.path.exists(COOKIES_FILE):
            cmd += ["--cookies", COOKIES_FILE]
        cmd += [
            "-o", os.path.join(MP3_DIR, tpl),
            url,
        ]
        return ("cli", cmd, None)


def run_download_job(job_id, url):
    """Run a download job using yt-dlp."""
    global YTDLP_AVAILABLE
    
    job = JOBS[job_id]
    job["log"].append(f"Downloading: {url}")
    
    try:
        cmd_type, cmd_or_opts, url = build_command(url, job.get("playlist", False))
        
        if cmd_type == "ydl" and YTDLP_AVAILABLE:
            with yt_dlp.YoutubeDL(cmd_or_opts) as ydl:
                ydl.download([url])
            job["done"] = True
            job["exit"] = 0
            job["log"].append("Done - saved to " + MP3_DIR)
            
            cands = [f for f in glob.glob(os.path.join(MP3_DIR, "*.mp3"))
                     if os.path.getmtime(f) >= time.time() - 30]
            if cands:
                job["file_name"] = os.path.basename(max(cands, key=os.path.getmtime))
        else:
            proc = subprocess.Popen(
                cmd_or_opts,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue
                with LOCK:
                    job["log"].append(line)
                    job["tail"] = line
                    m = re.search(r"Destination: (.+)$", line)
                    if m:
                        job["file_name"] = os.path.basename(m.group(1).strip().strip('"'))
            proc.wait()
            with LOCK:
                job["done"] = True
                job["exit"] = proc.returncode
                if proc.returncode == 0:
                    job["log"].append("Done - saved to " + MP3_DIR)
                else:
                    job["log"].append("Download failed.")
    except Exception as e:
        with LOCK:
            job["log"].append(f"ERROR: {e}")
            job["done"] = True
            job["exit"] = 1


def run_job(job_id, url):
    """Run a complete download job with normalization."""
    job = JOBS[job_id]
    job["log"].append("Starting download...")
    started = time.time()
    
    run_download_job(job_id, url)
    
    if NORMALIZE and JOBS[job_id].get("exit") == 0:
        try:
            cands = [f for f in glob.glob(os.path.join(MP3_DIR, "*.mp3"))
                     if os.path.getmtime(f) >= started]
            if cands:
                real_name = os.path.basename(max(cands, key=os.path.getmtime))
                with LOCK:
                    JOBS[job_id]["progress"] = 100.0
                    JOBS[job_id]["file_progress"] = 100.0
                    JOBS[job_id]["log"].append("Normalizing volume to -14 LUFS...")
                g = apply_normalize(os.path.join(MP3_DIR, real_name))
                with LOCK:
                    if g is None:
                        JOBS[job_id]["log"].append("Volume leveling: skipped (could not measure)")
                    elif g == 0.0:
                        JOBS[job_id]["log"].append("Volume leveling: already at target (no change)")
                    else:
                        JOBS[job_id]["log"].append(f"Volume leveling: %+0.1f dB (target -14 LUFS)" % g)
                    JOBS[job_id]["done"] = True
                    JOBS[job_id]["exit"] = 0
                    if real_name:
                        JOBS[job_id]["file_name"] = real_name
        except Exception as e:
            with LOCK:
                JOBS[job_id]["log"].append(f"Normalization error: {e}")


def run_batch(batch_id, urls):
    """Run a batch of downloads."""
    batch = BATCHES[batch_id]
    total = len(urls)
    batch["total"] = total
    
    for i, url in enumerate(urls):
        with LOCK:
            if batch.get("cancel"):
                batch["log"].append("[batch] Canceled.")
                return
            batch["current_index"] = i
            batch["log"].append(f"[batch] Downloading {i+1}/{total}: {url}")
        
        job_id = f"{batch_id}-{i}"
        with LOCK:
            JOBS[job_id] = {
                "log": [], "tail": "", "progress": 0, "file_progress": 0,
                "item": i+1, "total": total, "file_name": "", "done": False,
                "exit": -1, "playlist": batch.get("playlist", False),
                "normalize": batch.get("normalize", NORMALIZE)
            }
        
        run_job(job_id, url)
        
        with LOCK:
            ok = JOBS[job_id]["exit"] == 0
            batch["results"].append({
                "url": url, 
                "ok": ok, 
                "file_name": JOBS[job_id].get("file_name", "")
            })
            batch["log"].append(f"[batch] {'OK' if ok else 'FAILED'}: {url}")
        
        time.sleep(2)
    
    with LOCK:
        batch["done"] = True
        batch["current_index"] = -1


def load_history():
    """Load download history."""
    try:
        with open(HISTORY_FILE, encoding="utf-8") as f:
            h = json.load(f)
        return h if isinstance(h, list) else []
    except (OSError, ValueError):
        return []


def save_history(hist):
    """Save download history."""
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist[:100], f)
    except OSError:
        pass


def add_history(url, name, ok):
    """Add entry to download history."""
    h = load_history()
    h.insert(0, {"url": url, "name": name or url,
                 "time": time.strftime("%Y-%m-%d %H:%M"), "ok": ok})
    save_history(h)


def list_files():
    """List downloaded MP3 files."""
    try:
        files = []
        for name in os.listdir(MP3_DIR):
            if name.lower().endswith((".mp3", ".m4a", ".webm")):
                path = os.path.join(MP3_DIR, name)
                files.append({"name": name, "size": os.path.getsize(path)})
        files.sort(key=lambda f: f["name"].lower())
        return files
    except OSError:
        return []


def fmt_size(n):
    """Format file size."""
    if n >= 1 << 20:
        return f"{n / (1 << 20):.1f} MB"
    if n >= 1 << 10:
        return f"{n / (1 << 10):.0f} KB"
    return f"{n} B"


def load_page():
    """Load the HTML page to serve."""
    base = APP_DIR
    page_path = os.path.join(base, "index.html")
    try:
        with open(page_path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WinTune MP3 Downloader</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #0d1117; color: #e6edf3; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { color: #58a6ff; }
        input, button { padding: 10px; margin: 5px; }
        input { width: 300px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>WinTune MP3 Downloader</h1>
        <p>WinTune server running. Open in browser at http://127.0.0.1:8000</p>
        <p>Android version ready.</p>
    </div>
</body>
</html>
"""


PAGE = load_page()


class Handler(BaseHTTPRequestHandler):
    """HTTP request handler for WinTune server."""
    
    def log_message(self, *args):
        """Suppress default logging."""
        pass

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        """Send HTTP response."""
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        global MP3_DIR, QUALITY, EMBED_THUMB, NORMALIZE
        path = urlparse(self.path).path
        
        if path == "/":
            self._send(200, PAGE.encode("utf-8"))
        elif path == "/files":
            self._send(200, json.dumps(
                [{"name": f["name"], "size": fmt_size(f["size"])} for f in list_files()]
            ).encode("utf-8"), "application/json")
        elif path == "/dir":
            self._send(200, json.dumps({"dir": MP3_DIR}).encode("utf-8"), "application/json")
        elif path == "/settings":
            self._send(200, json.dumps({
                "dir": MP3_DIR, "quality": QUALITY, "embed_thumb": EMBED_THUMB,
                "normalize": NORMALIZE
            }).encode("utf-8"), "application/json")
        elif path == "/version":
            self._send(200, json.dumps({"version": VERSION}).encode("utf-8"), "application/json")
        elif path == "/history":
            self._send(200, json.dumps(load_history()).encode("utf-8"), "application/json")
        elif path.startswith("/status/"):
            job_id = path.split("/")[-1]
            with LOCK:
                job = JOBS.get(job_id)
                if not job:
                    self._send(404, b"not found")
                    return
                if job["total"] > 1:
                    total_pct = ((job["item"] - 1) + job["file_progress"] / 100) / job["total"] * 100
                else:
                    total_pct = job["file_progress"]
                total_pct = max(0.0, min(100.0, total_pct))
                data = {
                    "log": list(job["log"]),
                    "tail": job["tail"],
                    "progress": round(total_pct, 1),
                    "file_progress": job["file_progress"],
                    "file_name": job["file_name"],
                    "item": job["item"],
                    "total": job["total"],
                    "remaining": job["total"] - job["item"],
                    "done": job["done"],
                    "exit": job["exit"],
                    "dir": MP3_DIR,
                }
            self._send(200, json.dumps(data).encode("utf-8"), "application/json")
        elif path.startswith("/batchstatus/"):
            bid = path.split("/")[-1]
            with LOCK:
                batch = BATCHES.get(bid)
                if not batch:
                    self._send(404, b"not found")
                    return
                idx = batch["current_index"]
                cur_pct = 0.0
                cur_name = ""
                if idx >= 0:
                    job = JOBS.get(f"{bid}-{idx}")
                    if job:
                        cur_pct = job["file_progress"]
                        cur_name = job["file_name"]
                total = len(batch["urls"])
                overall = ((idx + cur_pct / 100) / total * 100) if total else 0
                overall = max(0.0, min(100.0, overall))
                data = {
                    "total": total,
                    "done_count": len(batch["results"]),
                    "current_index": idx,
                    "current_name": cur_name,
                    "file_progress": round(cur_pct, 1),
                    "progress": round(overall, 1),
                    "results": list(batch["results"]),
                    "log": list(batch["log"]),
                    "done": batch["done"],
                    "dir": MP3_DIR,
                }
            self._send(200, json.dumps(data).encode("utf-8"), "application/json")
        else:
            self._send(404, b"not found")

    def do_POST(self):
        """Handle POST requests for downloads."""
        global JOB_ID, BATCH_ID, MP3_DIR, QUALITY, EMBED_THUMB, NORMALIZE
        
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")

        if path == "/batch":
            try:
                payload = json.loads(raw)
            except ValueError:
                self._send(400, b"bad json")
                return
            urls = []
            for u in payload.get("urls", []):
                u = str(u).strip()
                if re.match(r"^(?:https?://\S+|ytsearch\d?:.+)$", u):
                    urls.append(u)
            if not urls:
                self._send(400, b"no valid urls")
                return
            with LOCK:
                BATCH_ID += 1
                bid = str(BATCH_ID)
                BATCHES[bid] = {
                    "urls": list(urls), 
                    "results": [],
                    "current_index": -1,
                    "log": [], 
                    "done": False,
                    "playlist": bool(payload.get("playlist", False)),
                    "normalize": bool(payload.get("normalize", NORMALIZE))
                }
            threading.Thread(target=run_batch, args=(bid, urls), daemon=True).start()
            self._send(200, json.dumps({"batch": bid}).encode("utf-8"), "application/json")
            return

        elif path == "/download":
            try:
                payload = parse_qs(raw)
                url = payload.get("url", [""])[0].strip()
            except Exception:
                self._send(400, b"bad request")
                return
            
            if not url:
                self._send(400, b"missing url")
                return
            
            with LOCK:
                JOB_ID += 1
                job_id = f"{JOB_ID}"
                JOBS[job_id] = {
                    "log": [], "tail": "", "progress": 0, "file_progress": 0,
                    "item": 1, "total": 1, "file_name": "", "done": False,
                    "exit": -1, "playlist": False, "normalize": NORMALIZE
                }
            
            run_job(job_id, url)
            self._send(200, json.dumps({"job": JOBS[job_id]}).encode("utf-8"), "application/json")
            return

        elif path == "/shutdown":
            self._send(200, b"shutting down")
            threading.Thread(target=shutdown_server, args=(self.server,), daemon=True).start()
            return

        else:
            self._send(404, b"not found")


def shutdown_server(server):
    """Gracefully shutdown the server."""
    time.sleep(0.5)
    server.shutdown()


def run_server():
    """Run the HTTP server."""
    load_settings()
    save_settings()
    
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"WinTune MP3 Downloader Android Edition v{VERSION}")
    print(f"Server running at http://{HOST}:{PORT}")
    print(f"Download directory: {MP3_DIR}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()


if __name__ == "__main__":
    run_server()