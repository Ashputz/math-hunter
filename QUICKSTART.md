# 🚀 QUICK START GUIDE

Panduan ringkas untuk test dan build Math Hunter Android app.

---

## ⚡ Test Locally (5 minutes)

### Step 1: Install Kivy
```bash
pip install kivy
```

### Step 2: Run App
```bash
python main.py
```

Game akan open dalam window. Test semua features!

---

## 📱 Build APK (Linux/Mac)

### Quick Build Commands
```bash
# Install buildozer (first time only)
pip install buildozer

# Build APK
buildozer android debug

# APK location: bin/mathhunter-1.0-debug.apk
```

**First build takes 20-40 minutes** (downloads Android SDK/NDK)
**Subsequent builds: 2-5 minutes**

---

## 🪟 Build APK (Windows)

### Option 1: Use WSL2
```bash
# Install WSL2 Ubuntu from Microsoft Store
# Then follow Linux commands above
```

### Option 2: Use Docker
```bash
# Install Docker Desktop
# Then run:
docker pull kivy/buildozer
docker run --rm -v "$(pwd)":/home/user/hostcwd kivy/buildozer buildozer android debug
```

---

## 📲 Install APK to Phone

### Simple Method:
1. Copy `bin/mathhunter-1.0-debug.apk` to phone
2. Open file manager
3. Tap APK file
4. Enable "Install from Unknown Sources" if asked
5. Install!

### Using ADB:
```bash
adb install bin/mathhunter-1.0-debug.apk
```

---

## 🎯 Key Features to Test

✅ **Main Menu**
- Play Game button
- Scoreboard button
- Settings button
- Credits button

✅ **Difficulty Selection**
- Easy (30 questions)
- Medium (50 questions)
- Hard (100 questions with timer)

✅ **Quiz Gameplay**
- Answer multiple choice questions
- See correct/wrong feedback
- Score tracking
- Timer countdown (Hard mode only)

✅ **Scoreboard**
- Top 10 high scores
- Name input for new records
- Date & time stamps
- Difficulty levels shown

✅ **Settings**
- Sound on/off toggle

---

## 🐛 Quick Troubleshooting

**App won't run locally?**
```bash
pip install --upgrade kivy
```

**Build fails?**
```bash
buildozer android clean
buildozer android debug
```

**APK won't install?**
- Check phone Android version (min 5.0)
- Enable "Unknown Sources" in Settings
- Try different APK (debug vs release)

**No sound?**
- Optional feature
- Works without sound files
- Add `ding.ogg` & `buzz.ogg` for sounds

---

## 📦 File Checklist

Essential files:
- ✅ `main.py` - Main app code
- ✅ `buildozer.spec` - Build config

Optional files:
- 📄 `scoreboard.json` - Auto-generated
- 🔊 `ding.ogg` - Correct answer sound
- 🔊 `buzz.ogg` - Wrong answer sound

---

## 💡 Pro Tips

1. **Test locally first** before building APK
2. **First build slow** - be patient!
3. **Use real device** - emulators slower
4. **Save build folder** - reuse for faster rebuilds
5. **Debug APK bigger** - release APK smaller

---

## 🎮 Gameplay Summary

1. Choose difficulty (Easy/Medium/Hard)
2. Answer math questions
3. Get instant feedback
4. Complete all questions
5. Submit score if Top 10!
6. Check scoreboard

**Hard Mode Challenge:**
- 15 seconds per question
- Wrong answer = restart entire quiz!
- Best for math masters 🧠

---

## 📊 Expected Results

**Desktop Test:**
- Opens in window
- Smooth animations
- All buttons work
- Scoreboard saves

**Android APK:**
- 60-80MB file size
- Installs in ~30 seconds
- Runs on Android 5.0+
- Touch-optimized UI

---

## 🎉 That's It!

Panduan lengkap ada dalam `README.md`

Selamat build! 🚀
