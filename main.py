"""
AbyssalSkillsD - Desktop Entrypoint
Initializes Desktop Window powered by Microsoft Edge WebView2 and PyWebView.
"""
import os
import sys
import ctypes
from pathlib import Path
import webview
from app.backend.api import DesktopAPI
from app.backend.paths import get_frontend_html, get_app_icon

def main():
    icon_ico = get_app_icon()
    
    # 1. Set explicit Windows AppUserModelID so the taskbar groups & displays the custom icon
    if sys.platform == "win32":
        try:
            app_id = "kyuu4.abyssalskillsd.ai.desktop.v1"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception:
            pass

        # High-Performance WebView2 Engine Optimization:
        # Isolates cache in Local AppData (avoids Defender locks in repo) & activates GPU acceleration
        try:
            webview_data_dir = Path.home() / "AppData" / "Local" / "AbyssalSkillsD" / "WebView2"
            webview_data_dir.mkdir(parents=True, exist_ok=True)
            os.environ["WEBVIEW2_USER_DATA_FOLDER"] = str(webview_data_dir)
            os.environ["WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS"] = (
                "--enable-gpu-rasterization --enable-zero-copy --disable-features=CalculateNativeWinOcclusion"
            )
        except Exception:
            pass

    api = DesktopAPI()
    
    # Path to frontend
    frontend_html = get_frontend_html()
    
    if not frontend_html.exists():
        print(f"Error: Frontend file not found at {frontend_html}")
        sys.exit(1)

    # Create Desktop Window (Edge WebView2)
    window = webview.create_window(
        title="AbyssalSkillsD — Quản Lý Kỹ Năng Cho Trợ Lý AI",
        url=str(frontend_html.as_uri()),
        js_api=api,
        width=1280,
        height=840,
        min_size=(960, 640),
        background_color="#050C1A"
    )

    # Start PyWebView loop with the official Abyssal Sky geometric icon
    icon_arg = str(icon_ico.resolve()) if icon_ico.exists() else None
    webview.start(debug=False, icon=icon_arg)

if __name__ == "__main__":
    main()
