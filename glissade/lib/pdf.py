import os
import shutil
import subprocess
from pathlib import Path


def get_pdf_export_style(base_style: str) -> str:
    """Return CSS tailored for PDF export: one slide per page, content-only rendering."""
    pdf_style = """
@media print {
    @page {
        margin: 0;
    }

    body {
        margin: 0 !important;
        padding: 0 !important;
        display: block !important;
        height: auto !important;
        overflow: visible !important;
        background: transparent !important;
    }

    nav {
        display: none !important;
    }

    .slides {
        margin: 0 !important;
        width: auto !important;
        height: auto !important;
        display: block !important;
        background: transparent !important;
    }

    .slide {
        position: static !important;
        top: auto !important;
        left: auto !important;
        transform: none !important;
        display: block !important;
        opacity: 1 !important;
        width: auto !important;
        max-width: none !important;
        aspect-ratio: auto !important;
        background: transparent !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        overflow: visible !important;
        margin: 0 !important;
        page-break-after: always;
        break-after: page;
    }

    .slide:last-child {
        page-break-after: auto;
        break-after: auto;
    }

    .slide-content {
        width: auto !important;
        height: auto !important;
        padding: 0.75in !important;
        overflow: visible !important;
        display: block !important;
    }

    footer {
        display: none !important;
    }
}
"""
    return base_style + "\n" + pdf_style


def _find_chromium_binary() -> str | None:
    """Return a Chromium-compatible browser binary path, or None if unavailable."""
    candidates = [
        os.environ.get("GLISSADE_CHROME_BIN", ""),
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]

    for candidate in candidates:
        if not candidate:
            continue
        if os.path.isabs(candidate) and os.path.exists(candidate):
            return candidate
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None


def export_pdf(html_path: str, pdf_path: str) -> None:
    """Export an HTML presentation to PDF using a Chromium-compatible headless browser."""
    browser = _find_chromium_binary()
    if not browser:
        raise RuntimeError(
            "No Chromium browser found. "
            "Install Chrome/Chromium or set GLISSADE_CHROME_BIN."
        )

    html_uri = Path(html_path).resolve().as_uri()
    pdf_output = str(Path(pdf_path).resolve())

    commands = [
        [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_output}",
            html_uri,
        ],
        [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_output}",
            html_uri,
        ],
    ]

    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0 and Path(pdf_output).exists():
            return

    raise RuntimeError(
        "Failed to export PDF via Chromium. "
        "Check that your browser supports --headless and --print-to-pdf."
    )
