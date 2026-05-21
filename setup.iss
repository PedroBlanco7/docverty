; Inno Setup Script — Docverty
; Genera: Docverty-Setup.exe
; Requiere Inno Setup 6+ (https://jrsoftware.org/isdl.php)

#define MyAppName      "Docverty"
#define MyAppVersion   "1.0"
#define MyAppExeName   "Docverty.exe"
#define MyAppPublisher "Pedro Blanco"
#define MyAppURL       ""

[Setup]
AppId={{A3F2C1D0-8B4E-4F2A-9C3D-1E5F6A7B8C9D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
SetupIconFile=icon.ico
OutputDir=installer
OutputBaseFilename=Docverty-Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
WizardResizable=no
MinVersion=10.0
PrivilegesRequired=admin
; LicenseFile=LICENSE.txt

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; \
  Description: "Crear acceso directo en el Escritorio"; \
  GroupDescription: "Iconos adicionales:"; \
  Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}";   DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico";                DestDir: "{app}"; Flags: ignoreversion
Source: "AVISOS-DE-TERCEROS.txt";  DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; \
  Filename: "{app}\{#MyAppExeName}"; \
  IconFilename: "{app}\icon.ico"; \
  WorkingDir: "{app}"
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\{#MyAppName}"; \
  Filename: "{app}\{#MyAppExeName}"; \
  IconFilename: "{app}\icon.ico"; \
  WorkingDir: "{app}"; \
  Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; \
  Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; \
  Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{app}"
