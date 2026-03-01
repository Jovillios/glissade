<div align="center">
  <img src="logo.svg" alt="glissade logo" width="128" height="128" />
</div>

# glissade

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/glissade.svg)](https://pypi.org/project/glissade/)

✨ Convert markdown files into **beautiful, interactive HTML slide presentations** — powered by [Catppuccin](https://catppuccin.com/) colors.

> No JavaScript frameworks. No build complexity. Pure, elegant slides.

---

## ✨ Features

- 🎨 **Catppuccin themes** — Five color palettes (default, frappe, latte, macchiato, mocha)
- ⌨️ **Keyboard navigation** — Arrow keys or h/l to move between slides
- 🔄 **Live mode** — Auto-reload while editing with `--live`
- 📄 **PDF export** — Generate slides as PDF with `--pdf`
- 🧭 **Optional navigation sidebar** — Jump to any slide instantly
- 📱 **Self-contained HTML** — No external dependencies, works offline
- 🐍 **Pure Python** — Simple, readable codebase

---

## Installation

Requires **Python 3.13+**.

```bash
# With uv (recommended)
uv add glissade

# With pip
pip install glissade
```

## Quick Start

### 1. Create `SLIDES.md`

```markdown
---
nav: true
theme: mocha
---

# Welcome 👋

This is the first slide.

---

# Second Slide

- Point A
- Point B
- Point C

---

# Thank you!
```

### 2. Build

```bash
glissade
```

### 3. Present

Open `index.html` in your browser and navigate with arrow keys or h/l.

## Writing Slides

### Slide Structure

Slides are separated by `---` on a line by itself. The first `---` block is reserved for YAML metadata.

```markdown
---
nav: true        # Optional metadata
theme: mocha
---

# Slide 1

Content...

---

# Slide 2

More content...
```

### Metadata (YAML Front Matter)

Configure your presentation with optional YAML at the top:

| Key | Default | Description |
|-----|---------|-------------|
| `nav` | `false` | Show navigation sidebar |
| `theme` | `default` | Color theme (see below) |

### Themes

Choose from **5 Catppuccin themes**:

| Theme | Description |
|-------|-------------|
| `default` | Original palette |
| `frappe` | Warm, frappé-inspired |
| `latte` | Light and airy |
| `macchiato` | Cool and balanced |
| `mocha` | Dark and rich |

### Markdown Support

Each slide supports standard markdown:

```markdown
# Headings

Regular paragraphs with **bold**, *italic*, and `inline code`.

- Bullet lists
- With multiple items

1. Numbered lists
2. Work too

> Blockquotes are supported

![Alt text becomes figcaption](https://example.com/image.jpg)
```

**Images** are wrapped in `<figure>` tags — alt text becomes figcaption.

### Navigation

Control your presentation:

- **← →** or **h / l** — Navigate slides
- **Click nav links** — Jump to any slide (when `nav: true`)

---

## Command Line Usage

```bash
glissade [OPTIONS]
```

### Common Options

| Option | Default | Description |
|--------|---------|-------------|
| `--input` | `SLIDES.md` | Markdown source file |
| `--output` | `index.html` | Output HTML file |
| `--live` | — | Start with live reload |
| `--port` | `8080` | Port for live server |
| `--pdf` | — | Also export as PDF |
| `--theme` | `default` | Override YAML theme |

### Advanced Options

| Option | Description |
|--------|-------------|
| `--template` | Custom main HTML template |
| `--slide-template` | Custom slide template |
| `--slides-template` | Custom slides container |
| `--style` | Custom CSS file |
| `--script` | Custom JavaScript file |

### Examples

```bash
# Standard build
glissade

# Custom files
glissade --input presentation.md --output slides.html

# Live editing (auto-reload)
glissade --live

# Live on custom port
glissade --live --port 3000

# Export to PDF
glissade --pdf presentation.pdf

# PDF only
glissade --output presentation.pdf
```

**Run as module:**
```bash
python -m glissade
```

### PDF Export

PDF export renders one page per slide (no navigation sidebar).
Requires a Chromium-compatible browser (`google-chrome`, `chromium`, etc.).

To specify a custom browser:
```bash
GLISSADE_CHROME_BIN=/path/to/chrome glissade --pdf output.pdf
```

### Live Reload

```bash
glissade --live
```

This:
1. Builds your presentation
2. Starts `http://localhost:8080`
3. Watches for file changes
4. Auto-rebuilds and reloads the browser
5. **Preserves your current slide** across reloads

---

## License

[MIT](LICENSE)
