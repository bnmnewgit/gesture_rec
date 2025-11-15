#!/bin/bash
echo "🔧 FIXING PYTHON PATH ISSUES"
echo "============================="

# Check if we're in the right virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ No virtual environment active!"
    echo "   Please run: source gesture_env/bin/activate"
    exit 1
fi

echo "✅ Virtual environment: $VIRTUAL_ENV"

# Find the correct site-packages path
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
SITE_PACKAGES="$VIRTUAL_ENV/lib/python$PYTHON_VERSION/site-packages"

echo "🔍 Python version: $PYTHON_VERSION"
echo "🔍 Site-packages: $SITE_PACKAGES"

# Check if site-packages exists
if [ ! -d "$SITE_PACKAGES" ]; then
    echo "❌ Site-packages directory not found: $SITE_PACKAGES"
    echo "   Creating directory..."
    mkdir -p "$SITE_PACKAGES"
fi

echo "📦 Checking installed packages in virtual environment..."
$VIRTUAL_ENV/bin/pip list | grep -E "(opencv|mediapipe|numpy)"

echo "🔗 Creating necessary symlinks..."

# Find system OpenCV and link it
SYSTEM_CV2=$(find /usr -name "cv2*" -type f 2>/dev/null | head -1)
if [ -n "$SYSTEM_CV2" ]; then
    echo "✅ Found system OpenCV: $SYSTEM_CV2"
    ln -sf "$SYSTEM_CV2" "$SITE_PACKAGES/cv2.so" 2>/dev/null && echo "✅ Created OpenCV symlink"
else
    echo "❌ No system OpenCV found"
fi

# Check if MediaPipe is in site-packages
MP_PATH=$(find "$SITE_PACKAGES" -name "mediapipe*" -type d 2>/dev/null | head -1)
if [ -n "$MP_PATH" ]; then
    echo "✅ MediaPipe found in virtual environment: $MP_PATH"
else
    echo "❌ MediaPipe not found in virtual environment"
    echo "   Reinstalling MediaPipe..."
    $VIRTUAL_ENV/bin/pip install mediapipe-rpi4 --no-cache-dir
fi

echo "🧪 Testing imports..."
python3 -c "
import sys
print('Python path:', sys.executable)

try:
    import cv2
    print('✅ OpenCV imported from:', cv2.__file__)
except Exception as e:
    print('❌ OpenCV import failed:', e)

try:
    import mediapipe as mp
    print('✅ MediaPipe imported from:', mp.__file__)
except Exception as e:
    print('❌ MediaPipe import failed:', e)

try:
    import numpy as np
    print('✅ NumPy imported from:', np.__file__)
except Exception as e:
    print('❌ NumPy import failed:', e)
"

echo ""
echo "============================="
echo "🎯 PATH FIX COMPLETED"
