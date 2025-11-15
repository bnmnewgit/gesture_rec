#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM DIAGNOSTIC
"""

import sys
import os
import subprocess

print("🔍 COMPREHENSIVE SYSTEM DIAGNOSTIC")
print("=" * 60)

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), -1

print("🐍 Python Environment:")
print(f"  Executable: {sys.executable}")
print(f"  Version: {sys.version}")
print(f"  Prefix: {sys.prefix}")
print(f"  Base Prefix: {sys.base_prefix}")
print(f"  Path: {sys.path}")

print("\n📦 Package Manager Info:")
pip_out, pip_err, _ = run_cmd(f"{sys.executable} -m pip --version")
print(f"  Pip: {pip_out}")

print("\n🔧 System Libraries:")
libs = ['libopenblas.so', 'libatlas.so', 'libgfortran.so', 'libquadmath.so']
for lib in libs:
    out, err, _ = run_cmd(f"ldconfig -p | grep {lib}")
    if out:
        print(f"  ✅ {lib}: Available")
    else:
        print(f"  ❌ {lib}: Missing")

print("\n📁 Critical Directories:")
dirs = [
    '/usr/lib',
    '/usr/local/lib', 
    sys.prefix + '/lib',
    '/lib'
]
for d in dirs:
    if os.path.exists(d):
        print(f"  ✅ {d}: Exists")
    else:
        print(f"  ❌ {d}: Missing")

print("\n🧪 Import Tests:")
import_tests = [
    'import numpy',
    'import cv2', 
    'import mediapipe'
]

for test in import_tests:
    try:
        exec(test)
        print(f"  ✅ {test}: SUCCESS")
    except ImportError as e:
        print(f"  ❌ {test}: FAILED - {e}")
    except Exception as e:
        print(f"  ⚠️  {test}: ERROR - {e}")

print("\n" + "=" * 60)
print("📊 DIAGNOSTIC COMPLETE")
