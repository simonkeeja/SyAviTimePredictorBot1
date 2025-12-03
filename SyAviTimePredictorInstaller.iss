[Setup]
AppName=SyAvi Time Predictor
AppVersion=1.0
DefaultDirName={autopf}\SyAviTimePredictor
DefaultGroupName=SyAvi Time Predictor
OutputBaseFilename={OUTPUT_FILENAME}
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\SyAviTimePredictorBot\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\SyAvi Time Predictor"; Filename: "{app}\SyAviTimePredictorBot.exe"
Name: "{userdesktop}\SyAvi Time Predictor"; Filename: "{app}\SyAviTimePredictorBot.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; Flags: unchecked

[Code]
const
  MASTER_KEY = '@Hg3505050';
  INSTALLER_SERIAL = '{SERIAL_NUMBER}';

function LockFileExists: Boolean;
var
  LockFile: String;
begin
  LockFile := ExpandConstant('{userappdata}\SyAviTimePredictor\machine.lock');
  Result := FileExists(LockFile);
end;

function CreateLockFile: Boolean;
var
  Dir: String;
  LockFile: String;
begin
  Dir := ExpandConstant('{userappdata}\SyAviTimePredictor');
  if not DirExists(Dir) then
    CreateDir(Dir);
  
  LockFile := Dir + '\machine.lock';
  Result := SaveStringToFile(LockFile, 'LOCKED', False);
end;

function DeleteLockFile: Boolean;
var
  LockFile: String;
begin
  LockFile := ExpandConstant('{userappdata}\SyAviTimePredictor\machine.lock');
  Result := DeleteFile(LockFile);
end;

function CheckMasterKey: Boolean;
var
  UserInput: String;
  AttemptCount: Integer;
begin
  Result := False;
  AttemptCount := 0;
  
  while AttemptCount < 3 do
  begin
    if InputQuery('Owner Bypass', 'This computer has already been installed on.' + #13#10 + 'Enter master key to bypass lock:', UserInput) then
    begin
      if UserInput = MASTER_KEY then
      begin
        Result := True;
        if DeleteLockFile then
          MsgBox('Lock removed successfully. Installation will proceed.', mbInformation, MB_OK)
        else
          MsgBox('Warning: Could not remove lock file, but proceeding anyway.', mbInformation, MB_OK);
        Exit;
      end
      else
      begin
        AttemptCount := AttemptCount + 1;
        if AttemptCount < 3 then
          MsgBox('Incorrect master key. Attempts remaining: ' + IntToStr(3 - AttemptCount), mbError, MB_OK)
        else
          MsgBox('Too many incorrect attempts. Installation cancelled.', mbError, MB_OK);
      end;
    end
    else
    begin
      Result := False;
      Exit;
    end;
  end;
end;

function InitializeSetup: Boolean;
begin
  Result := True;
  
  if LockFileExists then
  begin
    if not CheckMasterKey then
    begin
      MsgBox('Installation cancelled. This computer is already locked.', mbError, MB_OK);
      Result := False;
    end;
  end
  else
  begin
    if not CreateLockFile then
    begin
      MsgBox('Failed to activate this installation file.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;