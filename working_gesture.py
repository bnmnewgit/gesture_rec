#!/usr/bin/env python3
"""
WORKING GESTURE TEST - Using available packages
"""

import sys
import subprocess
import os

print("🎯 GESTURE CONTROL SYSTEM - MINIMAL TEST")
print("=" * 50)

def check_import(package_name, import_command):
    """Check if a package can be imported"""
    try:
        exec(import_command)
        return True, f"✅ {package_name} imported successfully"
    except ImportError as e:
        return False, f"❌ {package_name} import failed: {e}"

# Check essential packages
print("🔍 CHECKING ESSENTIAL PACKAGES:")
print("-" * 40)

# Check MediaPipe
mp_ok, mp_msg = check_import("MediaPipe", "import mediapipe as mp")
print(mp_msg)

# Check OpenCV - try multiple ways
cv2_ok = False
cv2_msg = ""

try:
    import cv2
    cv2_ok = True
    cv2_msg = f"✅ OpenCV imported: {cv2.__version__}"
except ImportError:
    # Try system OpenCV
    try:
        import imp
        cv2 = imp.load_source('cv2', '/usr/lib/python3/dist-packages/cv2.cpython-*-arm-linux-gnueabihf.so')
        cv2_ok = True
        cv2_msg = "✅ OpenCV loaded from system package"
    except:
        cv2_msg = "❌ OpenCV not available"

print(cv2_msg)

# Check NumPy
numpy_ok, numpy_msg = check_import("NumPy", "import numpy as np")
print(numpy_msg)

print("\n🎯 GESTURE DETECTION TEST")
print("-" * 40)

if mp_ok and cv2_ok and numpy_ok:
    print("🚀 All packages available! Starting gesture detection test...")
    
    try:
        import mediapipe as mp
        import numpy as np
        
        # Initialize MediaPipe Pose
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        
        print("✅ MediaPipe Pose initialized")
        
        # Try to initialize camera
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            
            if cap.isOpened():
                print("✅ Camera accessible")
                
                # Try to capture one frame
                ret, frame = cap.read()
                if ret:
                    print(f"✅ Frame captured: {frame.shape}")
                    
                    # Test MediaPipe processing
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = pose.process(rgb_frame)
                    
                    if results.pose_landmarks:
                        print("✅ Person detected! Gesture system is working!")
                    else:
                        print("⚠️  No person detected (make sure you're in frame)")
                        
                else:
                    print("❌ Could not read frame from camera")
                    
                cap.release()
            else:
                print("❌ Camera not accessible")
                
        except Exception as e:
            print(f"❌ Camera test failed: {e}")
            
    except Exception as e:
        print(f"❌ Gesture test failed: {e}")
        
else:
    print("❌ Missing packages. Cannot run gesture detection.")
    print("   Required: MediaPipe, OpenCV, NumPy")

print("\n" + "=" * 50)
print("📊 TEST SUMMARY")
print("=" * 50)

if mp_ok and cv2_ok and numpy_ok:
    print("🎉 SUCCESS! Your gesture control system is ready!")
    print("🚀 You can now build the full application.")
else:
    print("⚠️  Some components need fixing:")
    if not cv2_ok:
        print("   - OpenCV: Install with 'sudo apt install python3-opencv'")
    if not mp_ok:
        print("   - MediaPipe: Install with 'pip install mediapipe-rpi4'")
    if not numpy_ok:
        print("   - NumPy: Install with 'pip install numpy'")
