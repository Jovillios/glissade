import re
import markdown

from glissade import DATA_DIR
from glissade.lib.io import read_file, write_file
from glissade.lib.parser import parse_slide_classes


def convert_images_to_figures(html: str) -> str:
    """Convert <p><img alt="..." src="..."></p> to <figure><img ...><figcaption>alt</figcaption></figure>."""
    pattern = r'<p>\s*(<img\s+alt="([^"]*)"[^>]*>)\s*</p>'

    def replacer(match: re.Match) -> str:
        img_tag = match.group(1)
        alt_text = match.group(2)
        if alt_text:
            return f"<figure>{img_tag}<figcaption>{alt_text}</figcaption></figure>"
        return f"<figure>{img_tag}</figure>"

    return re.sub(pattern, replacer, html)


def fill_template(template: str, variables: dict[str, str]) -> str:
    return template.format(**variables)


def get_html_content(markdown_content: str, params: dict) -> str:
    """Convert markdown slides to full HTML content with navigation."""
    slide_template = read_file(params["slide_template"])
    slides_template = read_file(params["slides_template"])

    markdown_slides = markdown_content.split("---")
    slides_content: list[str] = []
    nav_content: list[str] = []
    num_slides = len(markdown_slides)

    for i, markdown_slide in enumerate(markdown_slides):
        extra_classes, markdown_slide = parse_slide_classes(markdown_slide)
        slide_content = markdown.markdown(markdown_slide)
        slide_content = convert_images_to_figures(slide_content)
        active = " active" if i == 0 else ""
        extra = " " + " ".join(extra_classes) if extra_classes else ""
        footer = f"{i + 1}/{num_slides}"
        html_slide = fill_template(
            slide_template,
            {
                "class": f"slide{active}{extra}",
                "index": f"{i}",
                "content": slide_content,
                "footer": footer,
            },
        )
        slides_content.append(html_slide)

        nav_content.append(
            f'<li><a href="#" class="nav-link{active}" data-slide="{i}">{i + 1}</a></li>'
        )

    class_nav = "hidden" if not params["nav"] else ""
    html_content = fill_template(
        slides_template,
        {
            "content": "\n".join(slides_content),
            "nav": "\n".join(nav_content),
            "class": class_nav,
        },
    )
    return html_content


def write_html(
    content: str, style: str, script: str, params: dict, live: bool = False
) -> None:
    """Render the final HTML file from content, style and script."""
    template_path = params["template"]
    output_path = params["output"]

    if live:
        live_reload_js = read_file(str(DATA_DIR / "scripts" / "live-reload.js"))
        script = script + "\n" + live_reload_js

    template = read_file(template_path)
    html_content = fill_template(
        template, {"content": content, "script": script, "style": style}
    )
    write_file(html_content, output_path)
