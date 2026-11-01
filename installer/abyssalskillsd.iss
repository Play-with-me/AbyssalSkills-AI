; =====================================================================
; AbyssalSkillsD - Inno Setup 6 Script
; Builds Windows standalone installer: AbyssalSkillsD-Setup-v1.0.1.exe
; =====================================================================

#define MyAppName "AbyssalSkillsD"
#define MyAppVersion "1.0.1"
#define MyAppPublisher "Lâm Nhựt Hải Đăng (Kyuu449977)"
#define MyAppURL "https://github.com/Play-with-me/AbyssalSkills-AI"
#define MyAppExeName "AbyssalSkillsD.exe"

[Setup]
AppId={{C74D2F20-1E4E-4B0D-8F7E-933B0A5F90B1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=..\dist
OutputBaseFilename=AbyssalSkillsD-Setup-v{#MyAppVersion}
SetupIconFile=..\app\frontend\assets\logo\app-icon.ico
UninstallDisplayName={#MyAppName} v{#MyAppVersion} - Enterprise AI Skill Studio
UninstallDisplayIcon={app}\{#MyAppExeName}
AppComments=Enterprise AI Skill Manager and Local-to-Cloud Marketplace for Cursor, Windsurf, Claude, and Copilot
VersionInfoDescription=AbyssalSkillsD Standalone Windows Installer
VersionInfoProductName={#MyAppName}
VersionInfoCompany={#MyAppPublisher}
VersionInfoVersion={#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "..\dist\AbyssalSkillsD\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
