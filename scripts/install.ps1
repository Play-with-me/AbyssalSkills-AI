<#
.SYNOPSIS
    AbyssalSkillsD Official Windows Dynamic Installer
.DESCRIPTION
    Automated 1-Click installer script for AbyssalSkillsD Enterprise AI Skill Studio.
    Dynamically discovers and downloads the latest official release directly from GitHub.
#>
[CmdletBinding()]
param(
    [switch]$Portable,
    [string]$Version = ""
)

$ErrorActionPreference = 'Stop'
$repo = "Play-with-me/AbyssalSkills-AI"

# Enforce secure TLS 1.2 / 1.3
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13

Write-Host ""
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host "   AbyssalSkillsD -- Enterprise AI Skill Studio Installer         " -ForegroundColor Magenta
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host ""

$tempDir = [System.IO.Path]::GetTempPath()
$targetTag = $Version
$downloadUrl = $null

# 1. Resolve Latest Version Dynamically
if (-not $targetTag) {
    Write-Host "[*] Đang truy vấn phiên bản mới nhất từ GitHub Releases..." -ForegroundColor Yellow
    try {
        $headers = @{
            "User-Agent" = "AbyssalSkillsD-Installer/1.0"
            "Accept"     = "application/vnd.github.v3+json"
        }
        $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/releases/latest" -Headers $headers -TimeoutSec 10 -ErrorAction Stop
        if ($release -and $release.tag_name) {
            $targetTag = $release.tag_name.TrimStart('v')
            Write-Host "[+] Phát hiện phiên bản mới nhất: v$targetTag" -ForegroundColor Green

            if ($Portable) {
                $asset = $release.assets | Where-Object { $_.name -like "*Portable.zip" } | Select-Object -First 1
                if ($asset) { $downloadUrl = $asset.browser_download_url }
            } else {
                $asset = $release.assets | Where-Object { $_.name -like "*Setup*.exe" } | Select-Object -First 1
                if ($asset) { $downloadUrl = $asset.browser_download_url }
            }
        }
    } catch {
        Write-Host "[!] Không thể truy vấn GitHub API (có thể do giới hạn kết nối). Sẽ sử dụng liên kết trực tiếp bản mới nhất." -ForegroundColor DarkGray
    }
}

# 2. Setup Download URLs and Destinations
if ($Portable) {
    $destPath = Join-Path $tempDir "AbyssalSkillsD-Portable.zip"
    if (-not $downloadUrl) {
        if ($targetTag) {
            $downloadUrl = "https://github.com/$repo/releases/download/v$targetTag/AbyssalSkillsD-Portable.zip"
        } else {
            $downloadUrl = "https://github.com/$repo/releases/latest/download/AbyssalSkillsD-Portable.zip"
        }
    }

    Write-Host "[*] Đang tải bản Portable mới nhất từ: $downloadUrl..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $destPath -UseBasicParsing
    } catch {
        Write-Host "[*] Thử lại qua liên kết dự phòng latest..." -ForegroundColor Yellow
        $fallbackUrl = "https://github.com/$repo/releases/latest/download/AbyssalSkillsD-Portable.zip"
        Invoke-WebRequest -Uri $fallbackUrl -OutFile $destPath -UseBasicParsing
    }

    Unblock-File -Path $destPath -ErrorAction SilentlyContinue

    $extractRoot = $env:USERPROFILE
    Write-Host "[*] Đang giải nén vào $extractRoot\AbyssalSkillsD..." -ForegroundColor Yellow
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
            Write-Host "[+] Đã tạo phím tắt trên màn hình chính (Desktop)." -ForegroundColor Cyan
        } catch {
            Write-Host "[!] Ghi chú: Chưa thể tự động tạo phím tắt desktop." -ForegroundColor DarkGray
        }

        Write-Host "[OK] Cài đặt AbyssalSkillsD Portable thành công tại: $appDir" -ForegroundColor Green
        Write-Host "[*] Đang khởi động AbyssalSkillsD..." -ForegroundColor Cyan
        Start-Process -FilePath $exePath -WorkingDirectory $appDir
    } else {
        Write-Host "[!] Lỗi: Không tìm thấy tệp AbyssalSkillsD.exe trong thư mục: $appDir" -ForegroundColor Red
    }
} else {
    $destPath = Join-Path $tempDir "AbyssalSkillsD-Setup.exe"
    if (-not $downloadUrl) {
        if ($targetTag) {
            $downloadUrl = "https://github.com/$repo/releases/download/v$targetTag/AbyssalSkillsD-Setup.exe"
        } else {
            $downloadUrl = "https://github.com/$repo/releases/latest/download/AbyssalSkillsD-Setup.exe"
        }
    }

    Write-Host "[*] Đang tải bản cài đặt Windows mới nhất từ: $downloadUrl..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $destPath -UseBasicParsing
    } catch {
        Write-Host "[*] Thử lại qua liên kết dự phòng latest..." -ForegroundColor Yellow
        $fallbackUrl = "https://github.com/$repo/releases/latest/download/AbyssalSkillsD-Setup.exe"
        Invoke-WebRequest -Uri $fallbackUrl -OutFile $destPath -UseBasicParsing
    }

    Unblock-File -Path $destPath -ErrorAction SilentlyContinue

    Write-Host "[OK] Đã tải xong trình cài đặt ($destPath)." -ForegroundColor Green
    Write-Host "[*] Đang mở trình hướng dẫn cài đặt AbyssalSkillsD..." -ForegroundColor Cyan
    Start-Process -FilePath $destPath
}
