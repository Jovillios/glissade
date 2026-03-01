# glissade

Convert markdown files into interactive HTML slide presentations.

## Installation

Requires **Python 3.13+**.

```bash
# With uv (recommended)
uv add glissade

# With pip
pip install glissade
```

## Quick Start

1. Create a `SLIDES.md` file:

```markdown
---
nav: true
theme: mocha
---

# Welcome

This is the first slide.

---

# Second Slide

- Point A
- Point B
- Point C

---

# Thank you!
```

2. Build the presentation:

```bash
glissade
```

3. Open `index.html` in a browser.

## Writing Slides

### Slide Separator

Slides are separated by `---` on its own line. The first `---` block at the top of the file is reserved for metadata.

### Metadata (YAML Front Matter)

Add optional YAML metadata between `---` markers at the top of the file:

```markdown
---
nav: true
theme: mocha
---
```

| Key     | Default     | Description                         |
|---------|-------------|-------------------------------------|
| `nav`   | `false`     | Show a navigation sidebar           |
| `theme` | `default`   | Color theme to use                  |

### Available Themes

All themes are based on [Catppuccin](https://github.com/catppuccin/catppuccin):

- `default` — Default palette
- `frappe` — Catppuccin Frappé
- `latte` — Catppuccin Latte
- `macchiato` — Catppuccin Macchiato
- `mocha` — Catppuccin Mocha

### Markdown Features

Each slide supports standard markdown:

```markdown
# Headings

Regular paragraphs with **bold**, *italic*, and `inline code`.

- Bullet lists
- With multiple items

1. Numbered lists
2. Work too

> Blockquotes are supported.

![Alt text becomes figcaption](https://example.com/image.jpg)
```

Images are automatically wrapped in `<figure>` tags. The alt text is used as `<figcaption>`.

### Navigation

In the generated presentation:

- **Arrow keys** (← →) or **h / l** — Navigate between slides
- **Click** nav links — Jump to a specific slide (when `nav: true`)

## CLI Usage

```
glissade [OPTIONS]
```

| Option               | Default              | Description                          |
|----------------------|----------------------|--------------------------------------|
| `--input`            | `SLIDES.md`          | Path to the markdown source file     |
| `--output`           | `index.html`         | Path for the generated HTML file     |
| `--template`         | *(bundled)*          | Custom main HTML template            |
| `--slide-template`   | *(bundled)*          | Custom individual slide template     |
| `--slides-template`  | *(bundled)*          | Custom slides container template     |
| `--style`            | *(bundled)*          | Custom base CSS file                 |
| `--script`           | *(bundled)*          | Custom JavaScript file               |
| `--pdf`              |                      | Export an additional PDF file        |
| `--live`             |                      | Start live mode with auto-reload     |
| `--port`             | `8080`               | Port for the live server             |

### Examples

```bash
# Build with default settings
glissade

# Custom input/output
glissade --input presentation.md --output slides.html

# Live mode — opens an HTTP server and rebuilds on file changes
glissade --live

# Live mode on a specific port
glissade --live --port 3000

# Build HTML + PDF
glissade --pdf slides.pdf

# Build PDF only
glissade --output slides.pdf
```

You can also run as a Python module:

```bash
python -m glissade
```

PDF export generates one page per slide and renders only slide content (no navigation sidebar or footer numbering).
It uses a Chromium-compatible browser in headless mode (`google-chrome`, `chromium`, etc.).
If needed, set `GLISSADE_CHROME_BIN` to the browser binary path.

## Live Mode

Pass `--live` to start a local HTTP server with automatic rebuild and browser reload:

```bash
glissade --live
```

This will:

1. Build the presentation
2. Start an HTTP server on `http://localhost:8080`
3. Watch source files for changes
4. Rebuild and reload the browser automatically when a file is modified

The current slide position is preserved across reloads.

## License

MIT
