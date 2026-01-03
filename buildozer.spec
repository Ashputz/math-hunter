[app]

# Title of your application
title = Math Hunter

# Package name
package.name = mathhunter

# Package domain (needed for android/ios packaging)
package.domain = com.azwan

# Source code where the main.py live
source.dir = .

# Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ogg,wav

# Version of your application
version = 1.0

# Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.10.8,kivy==2.1.0,sdl2_ttf==2.0.15,pillow,android

# Supported orientation (landscape, portrait or all)
orientation = portrait

# Android specific
[app:android]

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# API to use (must be >= 21)
android.api = 31

# Minimum API required
android.minapi = 21

# Android SDK version to use
android.sdk = 31

# Android NDK version to use
android.ndk = 25b

# Don't copy any libs
android.copy_libs = 0

# Android app theme
android.apptheme = "@android:style/Theme.NoTitleBar"

# Presplash background color (for background filling)
android.presplash_color = #19191e

# Presplash of the application
#android.presplash_filename = %(source.dir)s/data/presplash.png

# Icon of the application
#android.icon_filename = %(source.dir)s/data/icon.png

# Supported ABIs (armeabi-v7a, arm64-v8a, x86, x86_64)
android.archs = arm64-v8a


# Buildozer settings
[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1

# Build directory
build_dir = ./.buildozer

# Bin directory
bin_dir = ./bin
