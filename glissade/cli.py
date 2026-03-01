import argparse
import tempfile

from glissade import DATA_DIR
from glissade.lib.io import read_file
from glissade.lib.pdf import export_pdf, get_pdf_export_style
from glissade.lib.parser import parse_markdown_metadata
from glissade.lib.renderer import get_html_content, write_html
from glissade.lib.live import live_mode


def parse_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser("glissade")
    parser.add_argument("--input", default="SLIDES.md")
    parser.add_argument("--output", default="index.html")
    parser.add_argument(
        "--template", default=str(DATA_DIR / "templates" / "template.html")
    )
    parser.add_argument(
        "--slide-template", default=str(DATA_DIR / "templates" / "slide.html")
    )
    parser.add_argument(
        "--slides-template", default=str(DATA_DIR / "templates" / "slides.html")
    )
    parser.add_argument("--style", default=str(DATA_DIR / "style.css"))
    parser.add_argument("--script", default=str(DATA_DIR / "script.js"))
    parser.add_argument(
        "--live",
        action="store_true",
        help="Live mode: HTTP server + auto-reload",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for the live server (default: 8080)",
    )
    parser.add_argument(
        "--pdf",
        default=None,
        help="Path to the PDF to generate (export via Chromium headless)",
    )
    return parser.parse_args()


def build(params: dict) -> None:
    """Build the HTML presentation from source files."""
    raw_content = read_file(params["input"])
    metadata, markdown_content = parse_markdown_metadata(raw_content)
    params["nav"] = metadata.get("nav", False)
    content = get_html_content(markdown_content, params)

    theme_name = metadata.get("theme", "default")
    theme_css = read_file(str(DATA_DIR / "themes" / f"{theme_name}.css"))
    base_style = read_file(params["style"])
    style = theme_css + "\n" + base_style
    script = read_file(params["script"])

    output_path = params["output"]
    pdf_output = params.get("pdf")

    if not output_path.lower().endswith(".pdf"):
        write_html(content, style, script, params, live=params.get("live", False))
    else:
        pdf_output = output_path

    if pdf_output:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", prefix="glissade-pdf-", delete=True
        ) as temp_html:
            pdf_params = {**params, "output": temp_html.name}
            pdf_style = get_pdf_export_style(style)
            write_html(content, pdf_style, "", pdf_params, live=False)
            export_pdf(temp_html.name, pdf_output)


def main() -> None:
    args = parse_arg()
    params = vars(args)

    if params["live"] and (params.get("pdf") or params["output"].lower().endswith(".pdf")):
        raise SystemExit("--live est uniquement compatible avec une sortie HTML.")

    if params["live"]:
        live_mode(params, build)
    else:
        build(params)


if __name__ == "__main__":
    main()
