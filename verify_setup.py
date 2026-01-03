#!/usr/bin/env python3
"""
Math Hunter - Setup Verification Script
Run this to check if everything is ready before building APK
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} - Need Python 3.7+")
        return False

def check_kivy():
    """Check if Kivy is installed"""
    print("\n🔍 Checking Kivy installation...")
    try:
        import kivy
        print(f"  ✅ Kivy {kivy.__version__} - Installed")
        return True
    except ImportError:
        print("  ❌ Kivy not found")
        print("  💡 Install: pip install kivy")
        return False

def check_buildozer():
    """Check if Buildozer is installed"""
    print("\n🔍 Checking Buildozer installation...")
    try:
        import buildozer
        print(f"  ✅ Buildozer - Installed")
        return True
    except ImportError:
        print("  ⚠️  Buildozer not found (needed for APK build)")
        print("  💡 Install: pip install buildozer")
        return False

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking project files...")
    
    required_files = {
        'main.py': 'Main application',
        'buildozer.spec': 'Build configuration'
    }
    
    optional_files = {
        'ding.ogg': 'Correct answer sound',
        'buzz.ogg': 'Wrong answer sound'
    }
    
    all_ok = True
    
    for filename, description in required_files.items():
        if os.path.exists(filename):
            print(f"  ✅ {filename} - Found ({description})")
        else:
            print(f"  ❌ {filename} - MISSING! ({description})")
            all_ok = False
    
    for filename, description in optional_files.items():
        if os.path.exists(filename):
            print(f"  ✅ {filename} - Found ({description})")
        else:
            print(f"  ⚠️  {filename} - Optional ({description})")
    
    return all_ok

def test_import_main():
    """Try importing main.py"""
    print("\n🔍 Testing main.py imports...")
    try:
        # This will fail if there are syntax errors
        with open('main.py', 'r') as f:
            compile(f.read(), 'main.py', 'exec')
        print("  ✅ main.py syntax - Valid")
        return True
    except SyntaxError as e:
        print(f"  ❌ Syntax error in main.py: {e}")
        return False
    except FileNotFoundError:
        print("  ❌ main.py not found")
        return False

def check_platform():
    """Check operating system"""
    print("\n🔍 Checking platform...")
    if sys.platform.startswith('linux'):
        print("  ✅ Linux - Perfect for building APK")
    elif sys.platform == 'darwin':
        print("  ✅ macOS - Can build APK")
    elif sys.platform == 'win32':
        print("  ⚠️  Windows - Need WSL2 or Docker for APK build")
    else:
        print(f"  ⚠️  {sys.platform} - Unknown platform")

def main():
    """Run all checks"""
    print("=" * 60)
    print("Math Hunter - Setup Verification")
    print("=" * 60)
    
    results = []
    
    results.append(check_python_version())
    results.append(check_kivy())
    buildozer_ok = check_buildozer()
    results.append(check_files())
    results.append(test_import_main())
    check_platform()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    if all(results):
        print("✅ All checks passed!")
        print("\n📱 You can now:")
        print("  1. Test locally: python main.py")
        if buildozer_ok:
            print("  2. Build APK: buildozer android debug")
        else:
            print("  2. Install buildozer first: pip install buildozer")
    else:
        print("❌ Some checks failed!")
        print("\n🔧 Fix the issues above and run this script again")
        print("\n📖 For help, check:")
        print("  - README.md (detailed guide)")
        print("  - QUICKSTART.md (quick setup)")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
