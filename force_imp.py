#!/usr/bin/env python3
"""
FORCE CORRECT IMPORTS - Bypass path issues
"""

import sys
import os

print("🎯 FORCING CORRECT IMPORTS")
print("=" * 50)

# Add common package paths to sys.path
additional_paths = [
    "/usr/lib/python3/dist-packages",
    "/usr/local/lib/python3.11/dist-packages", 
    f"{sys.prefix}/lib/python3.11/site-packages",
    f"{sys.prefix}/lib/python3/site-packages"
]

print("➕ ADDING PATHS TO sys.path:")
for path in additional_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)
        print(f"   ✅ {path}")

print("\n🔍 CURRENT sys.path:")
for i, path in enumerate(sys.path[:10]):  # Show first 10
    print(f"   {i:2d}. {path}")

print("\n📦 ATTEMPTING IMPORTS WITH FORCED PATHS:")

# Try imports with explicit path checking
def force_import(module_name):
    """Force import a module by checking all possible paths"""
    print(f"\n🔍 Looking for {module_name}...")
    
    # Check all paths for the module
    for path in sys.path:
        potential_paths = [
            os.path.join(path, module_name),
            os.path.join(path, f"{module_name}.so"),
            os.path.join(path, f"{module_name}.cpython-*-arm-linux-gnueabihf.so")
        ]
        
        for potential in potential_paths:
            # Use glob for pattern matching
            import glob
            matches = glob.glob(potential)
            for match in matches:
                if os.path.exists(match):
                    print(f"   ✅ Found: {match}")
                    try:
                        # Try to load the module
                        if match.endswith('.so'):
                            import imp
                            module = imp.load_source(module_name, match)
                            return module, match
                        else:
                            __import__(module_name)
                            module = sys.modules[module_name]
                            return module, match
                    except Exception as e:
                        print(f"   ❌ Load failed: {e}")
    
    return None, None

# Try to force import OpenCV
cv2, cv2_path = force_import('cv2')
if cv2:
    print("🎉 OpenCV loaded successfully!")
    globals()['cv2'] = cv2
else:
    print("❌ Could not load OpenCV")

# Try to force import MediaPipe
mp, mp_path = force_import('mediapipe')
if mp:
    print("🎉 MediaPipe loaded successfully!")
    globals()['mp'] = mp
else:
    print("❌ Could not load MediaPipe")

# Regular numpy should work
try:
    import numpy as np
    print("✅ NumPy imported normally")
    globals()['np'] = np
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")

print("\n" + "=" * 50)
print("🧪 TESTING LOADED MODULES:")

if 'cv2' in globals():
    try:
        print(f"✅ OpenCV version: {cv2.__version__}")
    except:
        print("✅ OpenCV loaded but version check failed")

if 'mp' in globals():
    try:
        print(f"✅ MediaPipe version: {mp.__version__}")
    except:
        print("✅ MediaPipe loaded but version check failed")

if 'np' in globals():
    try:
        print(f"✅ NumPy version: {np.__version__}")
    except:
        print("✅ NumPy loaded but version check failed")

print("=" * 50)
