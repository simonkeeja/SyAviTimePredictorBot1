"""
SyAvi Time Predictor - Machine Unlock Utility
Owner Use Only - Master Key Required
Master Key: @Hg3505050
"""

import os
import sys
from pathlib import Path

MASTER_KEY = '@Hg3505050'

def get_lock_file_path():
    """Get the lock file path"""
    appdata = os.getenv('APPDATA')
    if not appdata:
        return None
    lock_file = os.path.join(appdata, 'SyAviTimePredictor', 'machine.lock')
    return lock_file

def main():
    """Main unlock utility"""
    print("\n" + "=" * 80)
    print("SyAvi Time Predictor - Machine Unlock Utility")
    print("Owner Use Only")
    print("=" * 80 + "\n")
    
    lock_file = get_lock_file_path()
    
    if not lock_file:
        print("✗ Error: Could not find AppData folder\n")
        sys.exit(1)
    
    print(f"Lock file location: {lock_file}\n")
    
    if not os.path.exists(lock_file):
        print("✓ No lock file found - this computer is already unlocked\n")
        print("=" * 80 + "\n")
        sys.exit(0)
    
    print("This computer is currently locked to an installation.\n")
    
    # Request master key
    print("Enter the Master Key to unlock this computer:")
    print("(This will allow you to reinstall the application)\n")
    
    key_input = input("Master Key: ").strip()
    
    if key_input != MASTER_KEY:
        print("\n✗ Invalid Master Key\n")
        print("=" * 80 + "\n")
        sys.exit(1)
    
    # Remove lock file
    try:
        os.remove(lock_file)
        print("\n✓ Lock file removed successfully!")
        print("✓ This computer is now unlocked")
        print("✓ You can now reinstall the application\n")
        print("=" * 80 + "\n")
    except Exception as e:
        print(f"\n✗ Error removing lock file: {e}\n")
        print("=" * 80 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
