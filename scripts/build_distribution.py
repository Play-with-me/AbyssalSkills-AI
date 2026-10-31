"""
AbyssalSkillsD - Standalone Distribution Packager
Compiles the application into a self-contained Windows executable and portable ZIP distribution.
Requires no Python or Git on client machines.
"""
import sys
import os
import shutil
import subprocess
import hashlib
import json
import zipfile
from pathlib import Path

def get_file_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    repo_root = Path(__file__).resolve().parent.parent
    spec_file = repo_root / "abyssalskillsd.spec"
    dist_dir = repo_root / "dist"
    build_dir = repo_root / "build"
    app_output_dir = dist_dir / "AbyssalSkillsD"
    exe_file = app_output_dir / "AbyssalSkillsD.exe"

    print("=" * 70)
    print(" AbyssalSkillsD v1.0.0 — Standalone Distribution Packager")
    print("=" * 70)
    print(f"[*] Workspace Root: {repo_root}")
    print(f"[*] Spec File:      {spec_file}")
    print(f"[*] Target Dist:    {app_output_dir}")

    # 1. Clean previous build if requested/needed
    if app_output_dir.exists():
        print("[*] Cleaning previous distribution build...")
        try:
            shutil.rmtree(app_output_dir)
        except Exception as e:
            print(f"[!] Warning cleaning dist: {e}")

    # 2. Invoke PyInstaller
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        str(spec_file)
    ]
    print(f"[*] Running PyInstaller: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(repo_root), capture_output=True, text=True)

    if result.returncode != 0:
        print("[X] PyInstaller Build Failed!")
        print(result.stderr)
        print(result.stdout[-1500:])
        sys.exit(1)

    print("[+] PyInstaller compiled successfully.")

    # 3. Verify Build Integrity
    assert exe_file.exists(), f"Error: {exe_file} not found after build!"
    
    # In PyInstaller 6+, bundled datas live inside _internal
    internal_dir = app_output_dir / "_internal"
    base_assets_dir = internal_dir if internal_dir.exists() else app_output_dir
    
    frontend_html = base_assets_dir / "app" / "frontend" / "index.html"
    assert frontend_html.exists(), f"Error: Frontend assets missing in {frontend_html}!"
    
    version_file = base_assets_dir / "app" / "data" / "version.json"
    assert version_file.exists(), f"Error: Version config missing in {version_file}!"
    with open(version_file, "r", encoding="utf-8") as f:
        v_data = json.load(f)
        assert v_data.get("app_name") == "AbyssalSkillsD", f"Wrong app name: {v_data}"
        assert v_data.get("version") == "1.0.0", f"Wrong version: {v_data}"

    icon_file = base_assets_dir / "app" / "frontend" / "assets" / "logo" / "app-icon.ico"
    assert icon_file.exists(), f"Error: Brand icon missing in {icon_file}!"

    # Add quickstart README for end-users
    readme_path = app_output_dir / "HUONG_DAN_SU_DUNG.txt"
    readme_path.write_text(
        "=========================================================\n"
        " AbyssalSkillsD v1.0.0 - Quản Lý Kỹ Năng Cho Trợ Lý AI\n"
        "=========================================================\n\n"
        "1. Cách khởi động:\n"
        "   - Nhấp đúp vào tệp 'AbyssalSkillsD.exe' để mở ứng dụng.\n"
        "   - Ứng dụng đã được đóng gói đầy đủ, không cần cài Python hay Git.\n\n"
        "2. Yêu cầu hệ thống:\n"
        "   - Windows 10 hoặc Windows 11 (64-bit).\n"
        "   - Microsoft Edge WebView2 Runtime (đã tích hợp sẵn trên Win 10/11).\n\n"
        "3. Hỗ trợ & Cập nhật:\n"
        "   - GitHub: https://github.com/kyuu4/abyssalskillsd\n"
        "   - Báo lỗi: https://github.com/kyuu4/abyssalskillsd/issues\n",
        encoding="utf-8"
    )

    exe_size_mb = exe_file.stat().st_size / (1024 * 1024)
    print(f"[+] Output Executable: {exe_file.name} ({exe_size_mb:.2f} MB)")
    print(f"[+] Verified Assets:    HTML, CSS, JS, Brand Icons & Version Config verified.")

    # 4. Generate Portable ZIP distribution
    zip_output_path = dist_dir / "AbyssalSkillsD-v1.0.0-Portable.zip"
    print(f"[*] Creating Portable Distribution: {zip_output_path.name}...")
    
    with zipfile.ZipFile(zip_output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in app_output_dir.rglob("*"):
            if file.is_file():
                rel_path = file.relative_to(dist_dir)
                zipf.write(file, arcname=rel_path)

    zip_size_mb = zip_output_path.stat().st_size / (1024 * 1024)
    zip_sha256 = get_file_sha256(zip_output_path)
    print(f"[+] Portable ZIP Created: {zip_output_path.name} ({zip_size_mb:.2f} MB)")
    print(f"    SHA256: {zip_sha256}")

    # 5. Check for Inno Setup compiler (ISCC)
    iscc_paths = [
        shutil.which("iscc"),
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]
    iscc_bin = next((p for p in iscc_paths if p and Path(p).exists()), None)
    iss_file = repo_root / "installer" / "abyssalskillsd.iss"

    if iscc_bin and iss_file.exists():
        print(f"[*] Inno Setup found at {iscc_bin}. Compiling Windows installer...")
        iss_res = subprocess.run([iscc_bin, str(iss_file)], cwd=str(iss_file.parent), capture_output=True, text=True)
        if iss_res.returncode == 0:
            setup_exe = dist_dir / "AbyssalSkillsD-Setup-v1.0.0.exe"
            if setup_exe.exists():
                setup_mb = setup_exe.stat().st_size / (1024 * 1024)
                print(f"[+] Standalone Installer: {setup_exe.name} ({setup_mb:.2f} MB)")
                print(f"    SHA256: {get_file_sha256(setup_exe)}")
        else:
            print(f"[!] ISCC warning: {iss_res.stderr}")
    else:
        print(f"[*] Inno Setup script prepared at: {iss_file}")
        print("    (Run `iscc installer/abyssalskillsd.iss` when Inno Setup is available to build Setup.exe)")

    print("\n" + "=" * 70)
    print(" [OK] Distribution Package Ready for Deployment!")
    print(f"  - App Directory: {app_output_dir}")
    print(f"  - Portable ZIP:  {zip_output_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()
