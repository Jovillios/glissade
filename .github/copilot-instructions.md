# Project Guidelines - glissade

## Overview
**glissade** is a Python tool that converts markdown files into interactive HTML slide presentations. It processes YAML metadata, parses markdown content, applies templates, and generates a self-contained HTML file with styling and keyboard navigation. It includes a **live mode** with a built-in HTTP server and auto-reload.

## Code Style
- **Type hints**: Use Python type annotations throughout (e.g., `def read_file(path: str) -> str`)
- **File I/O**: All file operations use simple `open()` with context managers
- **Template variables**: Use `str.format()` with dictionary unpacking for template substitution
- **Python version**: Target Python 3.13+ (see [pyproject.toml](pyproject.toml))

## Architecture

### Module Layout
```
glissade/            → Installable Python package
  __init__.py        → Package init, DATA_DIR constant
  __main__.py        → python -m glissade entry point
  cli.py             → CLI (argparse) + build() orchestration + main()
  lib/
    io.py            → read_file(), write_file()
    parser.py        → parse_markdown_metadata(), parse_markdown_comments(), parse_slide_classes()
    renderer.py      → get_html_content(), convert_images_to_figures(), fill_template(), write_html()
    live.py          → LiveHandler, live_mode(), file watcher (get_watched_files, get_mtimes)
  data/              → Bundled package data (templates, themes, scripts, CSS, JS)
    script.js        → Keyboard/click navigation
    style.css        → Base styles
    scripts/
      live-reload.js → Client-side polling script injected in live mode
    templates/       → template.html (main), slides.html (container), slide.html (individual)
    themes/          → Catppuccin CSS variants (default, frappe, latte, macchiato, mocha)
```

### Processing Pipeline (in `glissade/cli.py → build()`)

1. **Argument parsing** (`parse_arg()`) - CLI configuration for input/output paths, templates, and live mode
2. **Metadata extraction** (`glissade.lib.parser.parse_markdown_metadata()`) - Parses YAML front matter (between `---` markers) for options like `nav: true`, `theme: mocha`
3. **Markdown conversion** (`glissade.lib.renderer.get_html_content()`) - Splits slides by `---` separator, converts each to HTML, builds navigation
4. **Template rendering** (`glissade.lib.renderer.write_html()`) - Injects CSS, HTML content, JavaScript (and live-reload.js in live mode) into main template
5. **File I/O** (`glissade.lib.io.read_file()`, `glissade.lib.io.write_file()`) - Handle file reading/writing

Bundled data files (templates, themes, scripts) are resolved via `glissade.DATA_DIR`, a `Path` pointing to `glissade/data/`.

### Key Components
- **Input**: [SLIDES.md](SLIDES.md) - Markdown source with YAML metadata
- **Templates**: [glissade/data/templates/](glissade/data/templates/) - `template.html` (main), `slides.html` (container), `slide.html` (individual slide)
- **Styling**: [glissade/data/style.css](glissade/data/style.css) - Base styles; [glissade/data/themes/](glissade/data/themes/) - Catppuccin color variants
- **Client logic**: [glissade/data/script.js](glissade/data/script.js) - Keyboard/click navigation (arrow keys, h/l, mouse clicks)
- **Live reload**: [glissade/data/scripts/live-reload.js](glissade/data/scripts/live-reload.js) - Polls `/~version`, reloads on change, preserves current slide
- **Output**: [index.html](index.html) - Generated self-contained HTML

## Build and Test
Run with `uv`:
```bash
# Standard build (installed CLI)
uv run glissade [--input SLIDES.md] [--output index.html]

# As a Python module
uv run python -m glissade [--input SLIDES.md] [--output index.html]

# Live mode (HTTP server + auto-reload)
uv run glissade --live [--port 8080]

# Build the distributable package
uv build

# Install from wheel
pip install dist/glissade-*.whl
```

**No external tests**: The project uses manual HTML generation and browser verification. After running the tool, verify:
- All slides render correctly in `index.html`
- Navigation works (arrow keys, h/l keys, click nav links)
- Styles apply properly (Catppuccin colors)
- Metadata options (e.g., `nav: true`) take effect
- In live mode: editing source files triggers auto-rebuild and browser reload

## Project Conventions

### Markdown Input Structure
```markdown
---
nav: true          # Show navigation sidebar (optional)
---

# Slide 1
Content here

---

# Slide 2
More content
```

- **Slides are separated by `---`** on their own line
- **First slide uses H1** (`#`) for title
- **YAML metadata is optional** - defaults to `nav: false` if omitted

### HTML Comment Sections (Advanced)
The `parse_markdown_comments()` function supports nested `<!-- begin/end -->` tags for dynamic content areas:
```markdown
<!-- begin section-name -->
Dynamic content
<!-- end section-name -->
```
These are extracted into `result["areas"][name]` for custom processing (currently defined but not used in main pipeline).

### Template Variables
- **template.html**: `{content}`, `{style}`, `{script}`
- **slides.html**: `{content}`, `{nav}`, `{class}` (class="hidden" if nav disabled)
- **slide.html**: `{class}`, `{index}`, `{content}`, `{footer}` (shows "X/Total")

## Live Mode (`--live`)
When `--live` is passed:
1. `glissade/cli.py` calls `live_mode(params, build)` from `glissade.lib.live`
2. An initial `build()` is performed
3. A `http.server`-based HTTP server starts on `--port` (default 8080) in a daemon thread
4. A file watcher polls source files every 400ms; on change, `build()` re-runs and `_live_version` is incremented
5. `scripts/live-reload.js` is injected into the HTML — it polls `/~version` every 500ms and reloads the page when the version changes, preserving the current slide via `sessionStorage`

No external dependencies are used — everything relies on Python's stdlib (`http.server`, `threading`, `os.path.getmtime`).

## Integration Points
None - this is a standalone tool with no external APIs or integrations. Dependencies:
- **markdown** (3.10.2+) - Converts markdown to HTML

## Security
- No user authentication or sensitive data handling
- All file operations are local to the workspace
- HTML output is self-contained with no external script loading
