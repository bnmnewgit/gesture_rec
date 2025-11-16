# Cell 1: System Check and Package Installation
print("🎯 RASPBERRY PI 3 B+ - 32BIT OS GESTURE CONTROL PROJECT")
print("=" * 60)

# Check system information
import sys
import os
import platform

print("🔍 SYSTEM INFORMATION:")
print(f"Architecture: {platform.machine()}")
print(f"Python: {sys.version}")
print(f"OS: {platform.platform()}")
print(f"Working Directory: {os.getcwd()}")

# Install required packages
print("\n📦 INSTALLING REQUIRED PACKAGES...")
!pip install opencv-python-headless numpy matplotlib --index-url https://piwheels.org/simple --no-cache-dir

print("✅ Package installation completed")
