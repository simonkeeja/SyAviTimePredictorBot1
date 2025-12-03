"""
Generate Unique Customer Installers
Automatically creates fresh installers for each customer with unique serial numbers
Master Key: @Hg3505050
"""

import os
import subprocess
import uuid
from datetime import datetime
import sys

MASTER_KEY = '@Hg3505050'

def create_iss_content(output_name, serial_number):
    """Create ISS content programmatically"""
    lines = [
        "[Setup]",
        "AppName=SyAvi Time Predictor",
        "AppVersion=1.0",
        "DefaultDirName={autopf}\\SyAviTimePredictor",
        "DefaultGroupName=SyAvi Time Predictor",
        "OutputBaseFilename=" + output_name + "_Setup",
        "Compression=lzma",
        "SolidCompression=yes",
        "PrivilegesRequired=admin",
        "",
        "[Files]",
        'Source: "dist\\SyAviTimePredictorBot\\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs',
        "",
        "[Icons]",
        'Name: "{group}\\SyAvi Time Predictor"; Filename: "{app}\\SyAviTimePredictorBot.exe"',
        'Name: "{userdesktop}\\SyAvi Time Predictor"; Filename: "{app}\\SyAviTimePredictorBot.exe"; Tasks: desktopicon',
        "",
        "[Tasks]",
        'Name: "desktopicon"; Description: "Create a desktop icon"; Flags: unchecked',
        "",
        "[Code]",
        "const",
        "  MASTER_KEY = '@Hg3505050';",
        "  INSTALLER_SERIAL = '" + serial_number + "';",
        "",
        "function LockFileExists: Boolean;",
        "var",
        "  LockFile: String;",
        "begin",
        "  LockFile := ExpandConstant('{userappdata}\\SyAviTimePredictor\\machine.lock');",
        "  Result := FileExists(LockFile);",
        "end;",
        "",
        "function CreateLockFile: Boolean;",
        "var",
        "  Dir: String;",
        "  LockFile: String;",
        "begin",
        "  Dir := ExpandConstant('{userappdata}\\SyAviTimePredictor');",
        "  if not DirExists(Dir) then",
        "    CreateDir(Dir);",
        "  ",
        "  LockFile := Dir + '\\machine.lock';",
        "  Result := SaveStringToFile(LockFile, 'LOCKED', False);",
        "end;",
        "",
        "function InitializeSetup: Boolean;",
        "begin",
        "  Result := True;",
        "  ",
        "  if LockFileExists then",
        "  begin",
        "    MsgBox('Installation cancelled.' + #13#10 + #13#10 + 'This computer is already locked to one installation.' + #13#10 + 'To reinstall, please contact support.', mbError, MB_OK);",
        "    Result := False;",
        "  end",
        "  else",
        "  begin",
        "    if not CreateLockFile then",
        "    begin",
        "      MsgBox('Failed to activate this installation file.', mbError, MB_OK);",
        "      Result := False;",
        "    end;",
        "  end;",
        "end;",
    ]
    return "\n".join(lines)

def find_inno_setup():
    """Find Inno Setup compiler automatically"""
    possible_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    print("Searching for Inno Setup compiler...\n")
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Found Inno Setup at: {path}\n")
            return path
    
    search_dirs = [r"C:\Program Files", r"C:\Program Files (x86)"]
    
    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            try:
                for item in os.listdir(search_dir):
                    if "Inno Setup" in item:
                        compiler_path = os.path.join(search_dir, item, "ISCC.exe")
                        if os.path.exists(compiler_path):
                            print(f"✓ Found Inno Setup at: {compiler_path}\n")
                            return compiler_path
            except PermissionError:
                pass
    
    return None

def get_inno_setup_path():
    """Get Inno Setup path - auto-detect or ask user"""
    inno_path = find_inno_setup()
    if inno_path:
        return inno_path
    
    print("=" * 80)
    print("✗ Inno Setup Compiler Not Found")
    print("=" * 80)
    print("\nPlease enter the full path to ISCC.exe:")
    print("(Usually: C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe)\n")
    
    user_input = input("Enter path to ISCC.exe: ").strip().strip('"')
    
    if os.path.exists(user_input):
        print(f"\n✓ Found: {user_input}\n")
        return user_input
    else:
        print(f"\n✗ File not found: {user_input}")
        print("Download from: https://jrsoftware.org/isdl.php\n")
        sys.exit(1)

def verify_required_files():
    """Verify required files exist"""
    print("Verifying required files...\n")
    
    if os.path.exists('dist/SyAviTimePredictorBot/SyAviTimePredictorBot.exe'):
        print(f"✓ Application executable: dist/SyAviTimePredictorBot/SyAviTimePredictorBot.exe")
    else:
        print(f"✗ Application executable NOT FOUND")
        print("Run: python create_exe.py\n")
        sys.exit(1)
    
    print()

def generate_unique_serial():
    """Generate unique serial"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"SYA-{timestamp}-{unique_id}"

def create_customer_installer(customer_name, output_name, inno_compiler):
    """Create installer for customer"""
    if not output_name:
        output_name = customer_name.replace(" ", "_")
    
    serial_number = generate_unique_serial()
    
    print("=" * 80)
    print(f"GENERATING INSTALLER FOR: {customer_name}")
    print("=" * 80)
    print(f"Serial Number: {serial_number}")
    print(f"Output: {output_name}_Setup.exe")
    print()
    
    temp_iss_name = f"Setup_TEMP_{serial_number}.iss"
    
    iss_content = create_iss_content(output_name, serial_number)
    
    with open(temp_iss_name, "w", encoding='utf-8') as f:
        f.write(iss_content)
    
    print(f"✓ Created temporary setup: {temp_iss_name}")
    print(f"✓ Serial embedded: {serial_number}")
    print()
    
    output_dir = os.path.abspath("Output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Compiling with Inno Setup...")
    print(f"Output directory: {output_dir}")
    
    cmd = [
        inno_compiler,
        os.path.abspath(temp_iss_name),
        f'/O{output_dir}'
    ]
    
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        
        print("Inno Setup Output:")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        installer_path = os.path.join(output_dir, f"{output_name}_Setup.exe")
        
        if os.path.exists(installer_path):
            file_size = os.path.getsize(installer_path)
            print(f"✓ Compilation successful! ({file_size:,} bytes)")
        else:
            print("✗ Installer file not created!")
            if os.path.exists(temp_iss_name):
                os.remove(temp_iss_name)
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        if os.path.exists(temp_iss_name):
            os.remove(temp_iss_name)
        return False
    
    if os.path.exists(temp_iss_name):
        os.remove(temp_iss_name)
        print(f"✓ Cleaned up temporary files")
    
    print()
    print("=" * 80)
    print(f"✅ INSTALLER CREATED: {installer_path}")
    print(f"   Serial: {serial_number}")
    print(f"   Customer: {customer_name}")
    print("=" * 80)
    print()
    
    return serial_number

def main():
    """Main"""
    print("\n" + "🔧 " * 20)
    print("SyAvi Time Predictor - Customer Installer Generator")
    print("Master Key: @Hg3505050")
    print("🔧 " * 20 + "\n")
    
    verify_required_files()
    inno_compiler = get_inno_setup_path()
    
    print("=" * 80)
    print("CUSTOMER LIST")
    print("=" * 80 + "\n")
    
    customers = [
        ("Molaetsa Molaetsa", "Molaetsa"),
        ("Dollah Mod", "DollahMod"),
        ("Bame Bame ", "Bame"),
    ]
    
    print("Generating installers for:")
    for name, _ in customers:
        print(f"  • {name}")
    print()
    
    serials = {}
    successful = 0
    failed = 0
    
    for customer_name, output_name in customers:
        serial = create_customer_installer(customer_name, output_name, inno_compiler)
        if serial:
            serials[customer_name] = {'serial': serial, 'filename': f"{output_name}_Setup.exe"}
            successful += 1
        else:
            failed += 1
    
    print("\n" + "=" * 80)
    print("GENERATING MANIFEST")
    print("=" * 80)
    print()
    
    manifest_file = "OUTPUT_MANIFEST.txt"
    with open(manifest_file, "w", encoding='utf-8') as f:
        f.write("SyAvi Time Predictor - Customer Installation Manifest\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Master Key (Owner Use Only): {MASTER_KEY}\n")
        f.write(f"Total Installers: {successful} successful, {failed} failed\n\n")
        f.write("=" * 80 + "\n\n")
        
        if serials:
            for idx, (customer_name, info) in enumerate(serials.items(), 1):
                f.write(f"#{idx} Customer: {customer_name}\n")
                f.write(f"    Serial: {info['serial']}\n")
                f.write(f"    Filename: {info['filename']}\n")
                f.write(f"    Location: Output/{info['filename']}\n")
                f.write(f"    Status: Ready to distribute\n\n")
        else:
            f.write("ERROR: No installers were successfully created.\n")
    
    print(f"✓ Manifest saved: {manifest_file}\n")
    
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print(f"\nTotal Installers Created: {len(serials)}\n")
    
    if serials:
        print("✅ SUCCESS - All customer installers generated!\n")
        print("Installation Files (Output/):")
        for idx, (customer_name, info) in enumerate(serials.items(), 1):
            print(f"  {idx}. {customer_name}")
            print(f"     File: {info['filename']}")
            print(f"     Serial: {info['serial']}\n")
        print("Next: Send Output/[CustomerName]_Setup.exe to each customer")
    else:
        print("✗ FAILED - No installers created")
    
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()