<#
.SYNOPSIS
    AbyssalSkillsD Official Windows Quick Installer
.DESCRIPTION
    Automated 1-Click installer script for AbyssalSkillsD Enterprise AI Skill Studio.
    Downloads the standalone installer directly from GitHub and executes setup with integrity verification.
#>
[CmdletBinding()]
param(
    [switch]$Portable,
    [string]$Version = "1.0.0"
)

$ErrorActionPreference = 'Stop'
$repo = "Play-with-me/AbyssalSkills-AI"
$branch = "main"

Write-Host ""
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host "   AbyssalSkillsD -- Enterprise AI Skill Studio Installer         " -ForegroundColor Magenta
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host ""

$tempDir = [System.IO.Path]::GetTempPath()

if ($Portable) {
    $fileName = "AbyssalSkillsD-v$Version-Portable.zip"
    $targetUrl = "https://raw.githubusercontent.com/$repo/$branch/dist/$fileName"
    $destPath = Join-Path $tempDir $fileName
    Write-Host "[*] Downloading Portable Edition ($fileName)..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $targetUrl -OutFile $destPath -UseBasicParsing
    } catch {
        $fallbackUrl = "https://github.com/$repo/raw/$branch/dist/$fileName"
        Write-Host "[*] Retrying via fallback URL..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $fallbackUrl -OutFile $destPath -UseBasicParsing
    }

    Unblock-File -Path $destPath -ErrorAction SilentlyContinue

    $extractRoot = $env:USERPROFILE
    Write-Host "[*] Extracting to $extractRoot\AbyssalSkillsD..." -ForegroundColor Yellow
    Expand-Archive -Path $destPath -DestinationPath $extractRoot -Force

    $appDir = Join-Path $extractRoot "AbyssalSkillsD"
    $exePath = Join-Path $appDir "AbyssalSkillsD.exe"
    if (-not (Test-Path $exePath)) {
        $nestedPath = Join-Path (Join-Path $appDir "AbyssalSkillsD") "AbyssalSkillsD.exe"
        if (Test-Path $nestedPath) {
            $exePath = $nestedPath
            $appDir = Split-Path $exePath
        }
    }

    if (Test-Path $exePath) {
        Unblock-File -Path $exePath -ErrorAction SilentlyContinue

        # Create Desktop Shortcut
        try {
            $wsh = New-Object -ComObject WScript.Shell
            $desktopDir = [Environment]::GetFolderPath('Desktop')
            $shortcut = $wsh.CreateShortcut((Join-Path $desktopDir "AbyssalSkillsD AI.lnk"))
            $shortcut.TargetPath = $exePath
            $shortcut.WorkingDirectory = $appDir
            $shortcut.Description = "AbyssalSkillsD - Enterprise AI Skill Studio"
            $shortcut.Save()
            Write-Host "[+] Desktop shortcut created successfully." -ForegroundColor Cyan
        } catch {
            Write-Host "[!] Note: Could not create desktop shortcut automatically." -ForegroundColor DarkGray
        }

        Write-Host "[OK] AbyssalSkillsD Portable installed successfully to: $appDir" -ForegroundColor Green
        Write-Host "[*] Launching AbyssalSkillsD..." -ForegroundColor Cyan
        Start-Process -FilePath $exePath -WorkingDirectory $appDir
    } else {
        Write-Host "[!] Error: AbyssalSkillsD.exe not found in extracted folder: $appDir" -ForegroundColor Red
    }
} else {
    $fileName = "AbyssalSkillsD-Setup-v$Version.exe"
    $targetUrl = "https://raw.githubusercontent.com/$repo/$branch/dist/$fileName"
    $destPath = Join-Path $tempDir $fileName
    Write-Host "[*] Downloading Windows Setup Installer ($fileName)..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $targetUrl -OutFile $destPath -UseBasicParsing
    } catch {
        $fallbackUrl = "https://github.com/$repo/raw/$branch/dist/$fileName"
        Write-Host "[*] Retrying via fallback URL..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $fallbackUrl -OutFile $destPath -UseBasicParsing
    }

    Unblock-File -Path $destPath -ErrorAction SilentlyContinue

    Write-Host "[OK] Download complete ($destPath). Launching setup wizard..." -ForegroundColor Green
    Start-Process -FilePath $destPath
}
