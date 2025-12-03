"""
Android Machine Lock System for SyAvi Time Predictor
Handles device locking and serial verification
Works on both emulator and real Android devices
"""

import os
from pathlib import Path

class AndroidMachineLock:
    """Machine locking system for Android devices"""
    
    def __init__(self, app_serial=None):
        """Initialize with optional serial number"""
        self.app_serial = app_serial
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
            # Fallback for testing on desktop
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
            print(f"Error locking device: {e}")
            return False
    
    def verify_serial(self, serial):
        """Verify if serial matches locked device"""
        if not self.is_locked():
            # First install - lock to this serial
            return self.lock_device(serial)
        
        locked_serial = self.get_locked_serial()
        if locked_serial == serial:
            return True
        return False
    
    def get_status(self):
        """Get current lock status"""
        if self.is_locked():
            serial = self.get_locked_serial()
            return {
                'locked': True,
                'serial': serial,
                'message': f'This device is locked to serial: {serial}'
            }
        return {
            'locked': False,
            'serial': None,
            'message': 'Device is unlocked. Ready for first installation.'
        }
