"""Start the bundled app, check HTTP responses, and always stop its process."""
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent


def main():
    required = ["app.py", "data/podcasts_sample.csv", "pyproject.toml", "uv.lock"]
    for name in required:
        assert (ROOT / name).is_file(), name
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    with tempfile.TemporaryFile(mode="w+b") as log:
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true", "--server.address=127.0.0.1", f"--server.port={port}", "--browser.gatherUsageStats=false"],
            cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
        )
        try:
            deadline = time.monotonic() + 45
            while True:
                try:
                    with urllib.request.urlopen(f"http://127.0.0.1:{port}/_stcore/health", timeout=2) as response:
                        assert response.status == 200
                    break
                except (urllib.error.URLError, TimeoutError):
                    if process.poll() is not None or time.monotonic() >= deadline:
                        log.seek(0)
                        raise RuntimeError(log.read().decode(errors="replace"))
                    time.sleep(0.2)
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as response:
                assert response.status == 200
                assert response.read()
            print("Bundled files present: PASS")
            print("Streamlit health HTTP 200: PASS")
            print("Streamlit root HTTP 200: PASS")
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
        with socket.socket() as probe:
            probe.settimeout(2)
            assert probe.connect_ex(("127.0.0.1", port)) != 0, "Started port still open"
        print("Started server stopped and port closed: PASS")


if __name__ == "__main__":
    main()
