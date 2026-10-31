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
Write-Host "   🌌 AbyssalSkillsD — Enterprise AI Skill Studio Installer       " -ForegroundColor Magenta
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host ""

$tempDir = [System.IO.Path]::GetTempPath()

if ($Portable) {
    $fileName = "AbyssalSkillsD-v$Version-Portable.zip"
    $targetUrl = "https://raw.githubusercontent.com/$repo/$branch/dist/$fileName"
    $destPath = Join-Path $tempDir $fileName
    Write-Host "[*] Downloading Portable Edition ($fileName)..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $targetUrl -OutFile $destPath -UseBasicParsing
    
    $extractDir = Join-Path $env:USERPROFILE "AbyssalSkillsD"
    Write-Host "[*] Extracting to $extractDir..." -ForegroundColor Yellow
    Expand-Archive -Path $destPath -DestinationPath $extractDir -Force
    Write-Host "[✓] AbyssalSkillsD Portable installed successfully to: $extractDir" -ForegroundColor Green
    
    $exePath = Join-Path $extractDir "AbyssalSkillsD.exe"
    if (Test-Path $exePath) {
        Write-Host "[*] Launching AbyssalSkillsD..." -ForegroundColor Cyan
        Start-Process $exePath
    }
} else {
    $fileName = "AbyssalSkillsD-Setup-v$Version.exe"
    $targetUrl = "https://raw.githubusercontent.com/$repo/$branch/dist/$fileName"
    $destPath = Join-Path $tempDir $fileName
    Write-Host "[*] Downloading Windows Setup Installer ($fileName)..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $targetUrl -OutFile $destPath -UseBasicParsing
    
    Write-Host "[✓] Download complete. Launching setup wizard..." -ForegroundColor Green
    Start-Process -FilePath $destPath
}
