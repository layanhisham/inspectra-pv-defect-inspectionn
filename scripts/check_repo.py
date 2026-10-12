#!/usr/bin/env python3
"""Fail if the repository contains notebook outputs, private paths, identifiers,
embedded images or secrets. Run locally before pushing; also runs in CI.

    python scripts/check_repo.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()

TEXT_PATTERNS = {
    "Drive path outside the generic 'inspectra/' root": r"/content/drive/MyDrive/(?!inspectra/)",
    "local Windows/macOS user path": r"[A-Za-z]:\\\\Users|/Users/[A-Za-z0-9._-]+/|C:\\Users",
    "module/serial identifier (DTM...)": r"\bDTM\d{4,}",
    "possible API key / secret assignment": r"(?i)(api[_-]?key|secret|passwd|password|token)\s*[:=]\s*['\"][^'\"\s]{8,}",
    "Roboflow API key": r"\brf_[A-Za-z0-9]{16,}\b",
    "embedded base64 image": r"iVBORw0KGgo|/9j/4AAQ",
}
SKIP_DIRS = {".git", "_pending_approval", ".ipynb_checkpoints"}


def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        files = [ROOT / p for p in out.splitlines() if p]
        if files:
            return files
    except Exception:
        pass
    return [p for p in ROOT.rglob("*") if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS)]


def main():
    problems = []
    for f in tracked_files():
        if f == SELF or not f.exists():
            continue
        rel = f.relative_to(ROOT)
        if f.suffix in {".pt", ".pth", ".onnx", ".torchscript", ".tflite", ".h5", ".ckpt", ".safetensors"}:
            problems.append(f"{rel}: model weights must not be committed")
            continue
        if f.suffix.lower() in {".jpg", ".jpeg", ".bmp", ".tif", ".tiff"} or (
            f.suffix.lower() == ".png" and rel.parts[:2] != ("docs", "assets")
        ):
            problems.append(f"{rel}: image outside docs/assets (possible dataset image)")
            continue
        if f.suffix.lower() in {".png", ".zip", ".gz", ".tar"}:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        if f.suffix == ".ipynb":
            nb = json.loads(text)
            if set(nb.get("metadata", {})) - {"kernelspec", "language_info"}:
                problems.append(f"{rel}: extra notebook metadata (Colab/provenance)")
            for i, c in enumerate(nb.get("cells", [])):
                if c.get("cell_type") == "code" and (c.get("outputs") or c.get("execution_count") is not None):
                    problems.append(f"{rel}: cell {i} has outputs / execution count (clear all outputs)")
                if c.get("metadata"):
                    problems.append(f"{rel}: cell {i} has metadata")
        for name, pat in TEXT_PATTERNS.items():
            m = re.search(pat, text)
            if m:
                problems.append(f"{rel}: {name}: {m.group(0)[:60]!r}")
    if problems:
        print("Repository check FAILED:\n  - " + "\n  - ".join(problems))
        return 1
    print("Repository check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
