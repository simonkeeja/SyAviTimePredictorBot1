"""
PyInstaller Script - Create SyAviTimePredictorBot.exe
Run this on Windows to generate the executable for the installer
Master Key: @Hg3505050
"""

import PyInstaller.__main__
import os
import sys

def main():
    """Build the executable using PyInstaller"""
    
    print("\n" + "=" * 80)
    print("SyAvi Time Predictor - PyInstaller Build")
    print("=" * 80 + "\n")
    
    # Get absolute paths
    script_path = os.path.abspath("attached_assets/SyAviTimePredictorBot_1764276181880.py")
    bg_image = os.path.abspath("attached_assets/SyAviBackgroundPic.jpeg")
    icon_image = os.path.abspath("attached_assets/SyAviTimePredictorIcon_3D.png")
    
    # Verify all required files exist
    files_to_check = [
        ("Python Script", script_path),
        ("Background Image", bg_image),
        ("Icon Image", icon_image),
    ]
    
    all_exist = True
    for file_name, file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {file_name}: {file_path}")
        else:
            print(f"✗ {file_name} NOT FOUND: {file_path}")
            all_exist = False
    
    if not all_exist:
        print("\n✗ ERROR: Missing required files!")
        sys.exit(1)
    
    print("\n" + "-" * 80)
    print("Building executable...")
    print("-" * 80 + "\n")
    
    try:
        PyInstaller.__main__.run([
            script_path,
            '--name=SyAviTimePredictorBot',
            f'--icon={bg_image}',
            '--onedir',
            '--windowed',
            f'--add-data={bg_image}:.',
            f'--add-data={icon_image}:.',
            '--distpath=dist',
            '--workpath=build',
            '--specpath=.',
            '--noconfirm',
            '--clean',
        ])
        
        # Check if build was successful
        exe_path = os.path.join("dist", "SyAviTimePredictorBot", "SyAviTimePredictorBot.exe")
        
        if os.path.exists(exe_path):
            print("\n" + "=" * 80)
            print("✅ BUILD COMPLETE!")
            print("=" * 80)
            print(f"\nExecutable created: {exe_path}")
            print(f"\nOutput folder: dist/SyAviTimePredictorBot/")
            print("\n📝 Next Steps:")
            print("   1. Run: python generate_customer_installers.py")
            print("   2. Send Output/[CustomerName]_Setup.exe to each customer")
            print("=" * 80 + "\n")
        else:
            print("\n✗ ERROR: Executable was not created")
            sys.exit(1)
        
    except Exception as e:
        print(f"\n✗ BUILD FAILED!")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()