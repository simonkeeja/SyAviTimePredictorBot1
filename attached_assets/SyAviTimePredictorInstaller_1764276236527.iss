; SyAvi Time Predictor - One-Time Activation Installer

[Setup]
AppName=SyAvi Time Predictor
AppVersion=1.0
DefaultDirName={autopf}\SyAviTimePredictor
DefaultGroupName=SyAvi Time Predictor
OutputBaseFilename=SyAviTimePredictorSetup
Compression=lzma
SolidCompression=yes
WizardImageFile=SyAviBackgroundPic.jpeg
WizardSmallImageFile=SyAviTimePredictorIcon_3D.png
AllowNoIcons=yes
DisableStartupPrompt=yes
Uninstallable=yes

[Files]
Source: "..\dist\SyAviTimePredictorBot\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "SyAviBackgroundPic.jpeg"; DestDir: "{tmp}"; Flags: dontcopy noversioninfo
Source: "SyAviTimePredictorIcon_3D.png"; DestDir: "{tmp}"; Flags: dontcopy noversioninfo

[Icons]
Name: "{group}\SyAvi Time Predictor"; Filename: "{app}\SyAviTimePredictorBot.exe"; IconFilename: "{tmp}\SyAviTimePredictorIcon_3D.png"
Name: "{userdesktop}\SyAvi Time Predictor"; Filename: "{app}\SyAviTimePredictorBot.exe"; Tasks: desktopicon; IconFilename: "{tmp}\SyAviTimePredictorIcon_3D.png"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Code]
var
  LicenseKeyValid: Boolean;

function IsOwnerKey(Key: String): Boolean;
begin
  Result := Key = '@Hg3505050';
end;

function IsAlreadyInstalled: Boolean;
begin
  Result := FileExists(ExpandConstant('{userappdata}\SyAviTimePredictor\install.lock'));
end;

function SaveInstallMarker: Boolean;
var
  Dir: String;
begin
  Dir := ExpandConstant('{userappdata}\SyAviTimePredictor');
  if not DirExists(Dir) then
    ForceDirectories(Dir);
  Result := SaveStringToFile(Dir + '\install.lock', 'installed', False);
end;

function InitializeSetup: Boolean;
var
  UserKey: String;
begin
  Result := True;

  if IsAlreadyInstalled then
  begin
    MsgBox('This installer has already been used on this computer.', mbInformation, MB_OK);
    Result := False;
    exit;
  end;

  UserKey := '';
  if not InputQuery('SyAvi Time Predictor', 'Enter your license key:', UserKey) then
  begin
    Result := False;
    exit;
  end;

  if (Trim(UserKey) = '') or (not IsOwnerKey(UserKey)) then
  begin
    MsgBox('Invalid license key. Contact the developer to obtain a valid key.', mbError, MB_OK);
    Result := False;
    exit;
  end;

  LicenseKeyValid := True;

  if not SaveInstallMarker then
  begin
    MsgBox('Failed to save installation marker. Installation aborted.', mbError, MB_OK);
    Result := False;
    exit;
  end;
end;