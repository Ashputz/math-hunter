# Math Hunter - Android Version

Modern math quiz game untuk Android platform menggunakan Kivy framework.

## 📱 Features

### ✨ Gameplay
- **3 Difficulty Levels:**
  - Easy: 30 soalan mudah (1-12)
  - Medium: 50 soalan sederhana (10-50)
  - Hard: 100 soalan susah (20-100) dengan timer 15 saat

- **Quiz Features:**
  - Arithmetic operations: +, -, *, /, //
  - Multiple choice dengan 4 options
  - Instant feedback (correct/wrong)
  - Sound effects untuk jawapan
  - Timer countdown untuk Hard mode
  - Auto-restart quiz kalau salah jawab (Hard mode)

### 🏆 Scoreboard System
- Top 10 high scores
- Simpan nama, score, difficulty, tarikh & masa
- Persistent storage (JSON file)
- Color-coded rankings (Gold, Silver, Bronze)

### 🎨 Modern UI
- Dark theme dengan accent colors yang vibrant
- Touch-optimized buttons (large tap targets)
- Smooth screen transitions
- Material Design inspired
- Responsive layout untuk semua screen sizes

### ⚙️ Settings
- Toggle sound effects on/off
- Clean & simple interface

---

## 🚀 Setup & Installation

### Prerequisites

**Linux/Mac:**
```bash
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
```

**Windows:**
- Install Python 3.8+
- Install Git
- (Optional) Setup WSL2 untuk build Android APK

---

## 📦 Installation Steps

### 1. Clone/Download Project
```bash
cd /path/to/project
# Ensure you have main.py and buildozer.spec
```

### 2. Install Kivy
```bash
pip install kivy
```

### 3. Test Locally (Desktop)
```bash
python main.py
```

Game akan run dalam window. Test semua functionality sebelum build APK.

---

## 🔨 Building Android APK

### Method 1: Using Buildozer (Linux/Mac/WSL2)

#### Install Buildozer
```bash
pip install buildozer
pip install cython==0.29.33
```

#### Install Android Dependencies
```bash
sudo apt-get install -y \
    openjdk-11-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev
```

#### Build APK
```bash
# First time build (akan download SDK/NDK - ambil masa lama!)
buildozer android debug

# Subsequent builds (faster)
buildozer android debug

# Build for release (production)
buildozer android release
```

#### Output Location
APK file akan ada di: `bin/mathhunter-1.0-debug.apk`

---

### Method 2: Using Docker (Easiest for Windows)

#### Install Docker Desktop
Download dari: https://www.docker.com/products/docker-desktop

#### Build using Buildozer Docker Image
```bash
docker pull kivy/buildozer

docker run --rm -v "$(pwd)":/home/user/hostcwd kivy/buildozer \
    buildozer android debug
```

#### Get APK
APK akan ada dalam folder `bin/`

---

## 📲 Installing APK to Device

### Method 1: USB Connection
```bash
# Enable USB Debugging on phone first
# Settings > Developer Options > USB Debugging

# Install using ADB
adb install bin/mathhunter-1.0-debug.apk
```

### Method 2: Direct Transfer
1. Copy APK file ke phone
2. Open file manager
3. Tap APK file
4. Allow installation from unknown sources
5. Install

---

## 🎮 Testing Locally (Desktop)

Before building APK, test extensively on desktop:

```bash
python main.py
```

**Test Cases:**
- ✅ Main menu navigation
- ✅ All difficulty levels
- ✅ Quiz gameplay (30+ questions each)
- ✅ Timer functionality (Hard mode)
- ✅ Answer checking (correct/wrong)
- ✅ Score tracking
- ✅ Scoreboard save/load
- ✅ Name input
- ✅ Settings (sound toggle)
- ✅ Screen transitions

---

## 📁 Project Structure

```
math-hunter-android/
├── main.py              # Main application code
├── buildozer.spec       # Build configuration
├── scoreboard.json      # High scores (auto-generated)
├── ding.ogg            # Correct answer sound (optional)
├── buzz.ogg            # Wrong answer sound (optional)
└── README.md           # This file
```

---

## 🎵 Adding Sound Files (Optional)

Place these files in the same directory as `main.py`:

- `ding.ogg` - Correct answer sound effect
- `buzz.ogg` - Wrong answer sound effect

App akan function tanpa sound files, cuma takde sound effects je.

---

## 🐛 Common Issues & Solutions

### Issue 1: Buildozer fails on Windows
**Solution:** Use WSL2 or Docker method

### Issue 2: APK size too large (>80MB)
**Solution:** This is normal for Kivy apps (includes Python runtime)

### Issue 3: App crashes on startup
**Solution:** 
- Check Android version (min API 21 / Android 5.0)
- Rebuild: `buildozer android clean` then `buildozer android debug`

### Issue 4: Touch not responsive
**Solution:** Buttons sudah optimized untuk touch. Ensure tap within button area.

### Issue 5: Scoreboard not saving
**Solution:** 
- Check storage permissions in buildozer.spec
- Ensure `WRITE_EXTERNAL_STORAGE` permission granted

### Issue 6: First build takes forever
**Solution:** 
- Normal! First build downloads SDK/NDK (~2GB)
- Subsequent builds much faster
- Ensure stable internet connection

---

## 🎯 Optimization Tips

### For Better Performance:
1. Test on real device, not just emulator
2. Reduce animation complexity if laggy
3. Monitor memory usage for long quiz sessions

### For Smaller APK:
1. Remove unused imports
2. Use release build instead of debug
3. Enable ProGuard (advanced)

---

## 📊 APK Size Comparison

| Build Type | Size | Description |
|-----------|------|-------------|
| Debug | ~60-80MB | Includes debug symbols |
| Release | ~50-70MB | Optimized, no debug |
| Release + ProGuard | ~40-60MB | Maximum compression |

---

## 🔄 Update Version

To release new version:

1. Edit `buildozer.spec`:
```ini
version = 1.1
```

2. Update version in app:
```python
# In main.py, update version info if displayed
```

3. Rebuild:
```bash
buildozer android release
```

---

## 📝 Customization

### Change App Name
Edit `buildozer.spec`:
```ini
title = Your App Name
```

### Change Package Name
```ini
package.name = yourappname
package.domain = com.yourdomain
```

### Change Colors
Edit color values in `main.py`:
```python
# Search for Color definitions in GameData class
# Example: self.bg_color = Color(0.31, 0.98, 0.48, 1)
```

### Change Questions Count
Edit `DifficultyScreen` class in `main.py`:
```python
easy_btn.bind(on_press=lambda x: self.start_quiz(50, 'Easy'))  # Change 30 to 50
```

---

## 🆘 Support & Troubleshooting

### Kivy Documentation
https://kivy.org/doc/stable/

### Buildozer Documentation
https://buildozer.readthedocs.io/

### Common Commands

```bash
# Clean build files
buildozer android clean

# Update buildozer
pip install --upgrade buildozer

# Check buildozer version
buildozer --version

# Verbose build (for debugging)
buildozer -v android debug

# List connected devices
adb devices

# View app logs
adb logcat | grep python
```

---

## ✅ Pre-Release Checklist

Before releasing to users:

- [ ] Test all 3 difficulty levels
- [ ] Test scoreboard save/load
- [ ] Test on multiple devices (if possible)
- [ ] Test portrait orientation
- [ ] Verify app icon (if added)
- [ ] Test installation from APK
- [ ] Check app permissions
- [ ] Verify no crashes during gameplay
- [ ] Test timer functionality (Hard mode)
- [ ] Test sound effects
- [ ] Verify smooth screen transitions

---

## 🎓 Learning Resources

### Kivy Tutorials
- Official Kivy Tutorial: https://kivy.org/doc/stable/tutorials/
- Real Python Kivy Guide: https://realpython.com/mobile-app-kivy-python/

### Android Development
- Android Developer Guide: https://developer.android.com/

### Python Mobile Development
- Kivy Crash Course: https://www.youtube.com/results?search_query=kivy+tutorial

---

## 📄 License

Free to use and modify for personal projects.

---

## 👨‍💻 Developer

**Azwan Azli**

For questions or issues, refer to Kivy/Buildozer documentation.

---

## 🎉 Enjoy!

Game siap untuk dicompile dan test! Kalau ada issues, debug locally dulu sebelum build APK.

Good luck! 🚀
