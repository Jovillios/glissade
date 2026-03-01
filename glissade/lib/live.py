import os
import time
import threading
import functools
import http.server

from glissade import DATA_DIR
from glissade.lib.io import read_file
from glissade.lib.parser import parse_markdown_metadata


def get_watched_files(params: dict) -> list[str]:
    """Return the list of source files to watch for changes."""
    return [
        params["input"],
        params["style"],
        params["script"],
        params["template"],
        params["slide_template"],
        params["slides_template"],
    ]


def get_mtimes(files: list[str]) -> dict[str, float]:
    """Return a dict mapping each file to its last modification time."""
    mtimes: dict[str, float] = {}
    for f in files:
        try:
            mtimes[f] = os.path.getmtime(f)
        except OSError:
            mtimes[f] = 0
    return mtimes


# Version counter bumped on each rebuild (read by live-reload.js via /~version)
_live_version: int = 1


class LiveHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that serves files and exposes a /~version endpoint."""

    def do_GET(self) -> None:
        if self.path == "/~version":
            body = f'{{"v":{_live_version}}}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body.encode())
            return
        super().do_GET()

    def log_message(self, format: str, *args: object) -> None:
        pass


def live_mode(params: dict, build_fn: callable) -> None:
    """Start live mode: build, serve, watch, rebuild on changes."""
    global _live_version

    port = params["port"]
    output_dir = os.path.dirname(os.path.abspath(params["output"])) or "."

    # Initial build
    build_fn(params)
    print(f"\033[1;32m✓\033[0m Initial build completed → {params['output']}")
    print(f"\033[1;36m⟳\033[0m Live mode on http://localhost:{port}")
    print("  Ctrl+C to stop.\n")

    # Start HTTP server in a daemon thread
    handler = functools.partial(LiveHandler, directory=output_dir)
    server = http.server.HTTPServer(("", port), handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # Watch loop
    watched = get_watched_files(params)
    # Also watch theme file
    raw_content = read_file(params["input"])
    metadata, _ = parse_markdown_metadata(raw_content)
    theme_name = metadata.get("theme", "default")
    theme_file = str(DATA_DIR / "themes" / f"{theme_name}.css")
    if theme_file not in watched:
        watched.append(theme_file)

    last_mtimes = get_mtimes(watched)

    try:
        while True:
            time.sleep(0.4)
            current_mtimes = get_mtimes(watched)
            changed = [
                f for f in watched if current_mtimes[f] != last_mtimes.get(f, 0)
            ]
            if changed:
                last_mtimes = current_mtimes
                try:
                    build_fn(params)
                    _live_version += 1
                    names = ", ".join(os.path.basename(f) for f in changed)
                    print(f"\033[1;32m✓\033[0m Rebuild #{_live_version} ({names})")
                except Exception as e:
                    print(f"\033[1;31m✗\033[0m Error: {e}")
    except KeyboardInterrupt:
        print("\n\033[1;33m⏹\033[0m Shutting down live mode.")
        server.shutdown()
