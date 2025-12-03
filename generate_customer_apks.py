"""
Generate Unique Customer APKs for Android
Creates unique APKs with embedded serial numbers for machine locking
Master Key: @Hg3505050
"""

import os
import subprocess
import uuid
from datetime import datetime
import sys
import shutil
import re

MASTER_KEY = '@Hg3505050'

def generate_unique_serial():
    """Generate unique serial"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"SYA-{timestamp}-{unique_id}"

def modify_buildozer_spec(output_name, serial_number):
    """Modify buildozer.spec for customer"""
    spec_content = """[app]
title = SyAvi Time Predictor
package.name = syavitimepredictor
package.domain = org.syavi
version = 1.0
package.version = 1.0

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt

requirements = python3,kivy,android

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b

android.logcat_filters = *:S python:D
android.archs = arm64-v8a,armeabi-v7a

p4a.dir = %(source.dir)s/.buildozer/android/platform/build-{{ arch }}/packages/python-for-android
p4a.url = https://github.com/kivy/python-for-android/archive/develop.zip

[buildozer]
log_level = 2
warn_on_root = 1
"""
    return spec_content

def modify_android_lock(serial_number):
    """Create customer-specific android_machine_lock.py with serial embedded"""
    lock_code = f'''"""
Android Machine Lock System for SyAvi Time Predictor
Customer: SyAvi Time Predictor
Serial: {serial_number}
Master Key: @Hg3505050
"""

import os

class AndroidMachineLock:
    """Machine locking system for Android devices"""
    
    INSTALLER_SERIAL = "{serial_number}"
    MASTER_KEY = "@Hg3505050"
    
    def __init__(self, app_serial=None):
        """Initialize with serial number"""
        self.app_serial = app_serial or self.INSTALLER_SERIAL
        self.lock_dir = self.get_app_data_dir()
        self.lock_file = os.path.join(self.lock_dir, 'machine.lock')
    
    @staticmethod
    def get_app_data_dir():
        """Get application data directory on Android"""
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            context = activity.getApplicationContext()
            files_dir = context.getFilesDir()
            return str(files_dir.getAbsolutePath())
        except:
            home = os.path.expanduser('~')
            app_data = os.path.join(home, '.syavi_time_predictor')
            os.makedirs(app_data, exist_ok=True)
            return app_data
    
    def is_locked(self):
        """Check if device is locked"""
        return os.path.exists(self.lock_file)
    
    def get_locked_serial(self):
        """Get the serial number this device is locked to"""
        if self.is_locked():
            try:
                with open(self.lock_file, 'r') as f:
                    return f.read().strip()
            except:
                return None
        return None
    
    def lock_device(self, serial):
        """Lock device to this serial number"""
        try:
            os.makedirs(self.lock_dir, exist_ok=True)
            with open(self.lock_file, 'w') as f:
                f.write(serial)
            return True
        except Exception as e:
            print(f"Error locking device: {{e}}")
            return False
    
    def verify_serial(self, serial):
        """Verify if serial matches locked device"""
        if not self.is_locked():
            return self.lock_device(self.INSTALLER_SERIAL)
        
        locked_serial = self.get_locked_serial()
        if locked_serial == self.INSTALLER_SERIAL:
            return True
        return False
    
    def get_status(self):
        """Get current lock status"""
        if self.is_locked():
            serial = self.get_locked_serial()
            return {{
                'locked': True,
                'serial': serial,
                'message': f'Device locked to: {{serial}}'
            }}
        return {{
            'locked': False,
            'serial': None,
            'message': 'Ready for installation'
        }}
'''
    return lock_code

def build_apk_with_buildozer(customer_name, serial_number, output_name):
    """Build APK using buildozer"""
    print(f"\n{'='*80}")
    print(f"Building APK for: {customer_name}")
    print(f"Serial: {serial_number}")
    print(f"{'='*80}\n")
    
    # Create temporary build directory
    build_dir = f"build_{output_name}"
    
    try:
        # Copy necessary files
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        
        # Copy main app files
        shutil.copy('main.py', os.path.join(build_dir, 'main.py'))
        shutil.copy('attached_assets/SyAviBackgroundPic.jpeg', os.path.join(build_dir, 'SyAviBackgroundPic.jpeg'))
        shutil.copy('attached_assets/SyAviTimePredictorIcon_3D.png', os.path.join(build_dir, 'SyAviTimePredictorIcon_3D.png'))
        
        # Create customer-specific lock file
        lock_code = modify_android_lock(serial_number)
        with open(os.path.join(build_dir, 'android_machine_lock.py'), 'w') as f:
            f.write(lock_code)
        
        # Create buildozer.spec
        spec_content = modify_buildozer_spec(output_name, serial_number)
        with open(os.path.join(build_dir, 'buildozer.spec'), 'w') as f:
            f.write(spec_content)
        
        print(f"✓ Created build directory: {build_dir}")
        print(f"✓ Copied app files")
        print(f"✓ Embedded serial: {serial_number}")
        print(f"\nTo build APK, run from {build_dir}:")
        print(f"  cd {build_dir}")
        print(f"  buildozer android release")
        print(f"\nAPK will be created at:")
        print(f"  {build_dir}/bin/{output_name}-1.0-release.apk")
        
        return True
        
    except Exception as e:
        print(f"✗ Error building APK: {e}")
        return False

def main():
    """Main"""
    print("\n" + "🔨 " * 20)
    print("SyAvi Time Predictor - Android APK Generator")
    print("Master Key: @Hg3505050")
    print("🔨 " * 20 + "\n")
    
    if not os.path.exists('main.py'):
        print("✗ main.py not found!")
        print("Make sure you have copied the Kivy app as main.py")
        sys.exit(1)
    
    print("=" * 80)
    print("CUSTOMER LIST")
    print("=" * 80 + "\n")
    
    customers = [
        ("Simon Keeja", "SimonKeeja"),
        ("Keitumetse Duta", "KeitumetseDuta"),
        ("Jayden Duta", "JaydenDuta"),
    ]
    
    print("Generating APKs for:")
    for name, _ in customers:
        print(f"  • {name}")
    print()
    
    manifest_data = []
    
    for customer_name, output_name in customers:
        serial = generate_unique_serial()
        
        if build_apk_with_buildozer(customer_name, serial, output_name):
            manifest_data.append({
                'name': customer_name,
                'output': output_name,
                'serial': serial
            })
    
    # Create manifest
    print("\n" + "=" * 80)
    print("GENERATING MANIFEST")
    print("=" * 80 + "\n")
    
    manifest_file = "APK_MANIFEST.txt"
    with open(manifest_file, "w", encoding='utf-8') as f:
        f.write("SyAvi Time Predictor - Android APK Manifest\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Master Key (Owner Use Only): {MASTER_KEY}\n")
        f.write(f"Total APKs: {len(manifest_data)}\n\n")
        f.write("=" * 80 + "\n\n")
        
        for idx, data in enumerate(manifest_data, 1):
            f.write(f"#{idx} Customer: {data['name']}\n")
            f.write(f"    Serial: {data['serial']}\n")
            f.write(f"    Output Name: {data['output']}\n")
            f.write(f"    Build Directory: build_{data['output']}\n")
            f.write(f"    APK Location: build_{data['output']}/bin/{data['output']}-1.0-release.apk\n")
            f.write(f"    Status: Ready to build\n\n")
    
    print(f"✓ Manifest saved: {manifest_file}\n")
    
    print("\n" + "=" * 80)
    print("BUILD INSTRUCTIONS")
    print("=" * 80)
    print("\nFor each customer, run:\n")
    
    for data in manifest_data:
        print(f"  cd build_{data['output']}")
        print(f"  buildozer android release")
        print(f"  # APK created: bin/{data['output']}-1.0-release.apk")
        print()
    
    print("Then distribute the APK files to customers.\n")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
