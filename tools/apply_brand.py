#!/usr/bin/env python3
"""Safely inject the shared 3Parusa brand assets into secondary HTML pages.

The default mode is a read-only preview. Pass ``--write`` to apply atomic,
idempotent updates, or ``--self-test`` to exercise only in-memory strings.
"""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote


SITE_ORIGIN = "https://3parusa.ru"
BRAND_OG_URL = f"{SITE_ORIGIN}/assets/brand/og.png"
CSS_HREF = "/assets/brand/brand.css"
SCRIPT_SRC = "/assets/brand/enhance.js"

CSS_TAG = f'<link rel="stylesheet" href="{CSS_HREF}">'.encode("ascii")
SCRIPT_TAG = f'<script src="{SCRIPT_SRC}" defer></script>'.encode("ascii")
OG_TAG = f'<meta property="og:image" content="{BRAND_OG_URL}">'.encode("ascii")
TWITTER_TAG = b'<meta name="twitter:card" content="summary_large_image">'

HEAD_CLOSE_RE = re.compile(br"</head\s*>", re.IGNORECASE)
OG_IMAGE_RE = re.compile(
    br"<meta\b[^>]*\b(?:property|name)\s*=\s*([\"'])og:image\1[^>]*>",
    re.IGNORECASE,
)
TWITTER_CARD_RE = re.compile(
    br"<meta\b[^>]*\bname\s*=\s*([\"'])twitter:card\1[^>]*>",
    re.IGNORECASE,
)
CANONICAL_RE = re.compile(
    br"<link\b[^>]*\brel\s*=\s*([\"'])[^\"']*\bcanonical\b[^\"']*\1[^>]*>",
    re.IGNORECASE,
)
CSS_RE = re.compile(
    br"<link\b[^>]*\bhref\s*=\s*([\"'])/assets/brand/brand\.css(?:\?[^\"']*)?\1[^>]*>",
    re.IGNORECASE,
)
SCRIPT_RE = re.compile(
    br"<script\b[^>]*\bsrc\s*=\s*([\"'])/assets/brand/enhance\.js(?:\?[^\"']*)?\1[^>]*>",
    re.IGNORECASE,
)

EXCLUDED_DIRECTORIES = {".git", "assets", "tools", "work", "outputs"}
EXCLUDED_ROOT_FILES = {"index.html", "index.tilda-original.html"}


class BrandInjectionError(ValueError):
    """Raised when an HTML document cannot be updated without guessing."""


def canonical_url(relative_path: Path) -> str:
    """Return the public self-canonical URL for a repository-relative page."""

    relative = relative_path.as_posix().lstrip("/")
    if relative.lower().endswith("/index.html"):
        route = "/" + relative[: -len("index.html")]
    else:
        route = "/" + relative
    return SITE_ORIGIN + quote(route, safe="/-._~")


def _canonical_tag(url: str) -> bytes:
    return f'<link rel="canonical" href="{url}">'.encode("ascii")


def _newline_for(document: bytes) -> bytes:
    return b"\r\n" if b"\r\n" in document else b"\n"


def inject_brand(document: bytes, page_canonical: str) -> tuple[bytes, bool]:
    """Return ``(updated_document, changed)`` without mutating external state."""

    additions: list[bytes] = []
    has_og_image = bool(OG_IMAGE_RE.search(document))

    if not has_og_image:
        additions.append(OG_TAG)
        if not TWITTER_CARD_RE.search(document):
            additions.append(TWITTER_TAG)
    if not CANONICAL_RE.search(document):
        additions.append(_canonical_tag(page_canonical))
    if not CSS_RE.search(document):
        additions.append(CSS_TAG)
    if not SCRIPT_RE.search(document):
        additions.append(SCRIPT_TAG)

    if not additions:
        return document, False

    closing_head = HEAD_CLOSE_RE.search(document)
    if not closing_head:
        raise BrandInjectionError("missing </head> marker")

    newline = _newline_for(document)
    before = document[: closing_head.start()]
    after = document[closing_head.start() :]
    leading_newline = b"" if before.endswith((b"\n", b"\r")) else newline
    insertion = leading_newline + newline.join(additions) + newline
    return before + insertion + after, True


def iter_secondary_pages(root: Path) -> list[Path]:
    """Discover public secondary HTML pages while excluding assets and backups."""

    pages: list[Path] = []
    for path in root.rglob("*.html"):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0].lower() in EXCLUDED_DIRECTORIES:
            continue
        if len(relative.parts) == 1 and relative.name.lower() in EXCLUDED_ROOT_FILES:
            continue
        pages.append(path)
    return sorted(pages, key=lambda item: item.relative_to(root).as_posix().lower())


def _atomic_write(path: Path, payload: bytes) -> None:
    """Replace one file atomically while preserving its permission bits."""

    original_mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.brand-",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary_path, original_mode)
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def process_pages(root: Path, *, write: bool) -> tuple[list[Path], list[tuple[Path, str]]]:
    """Preview or apply all required updates below ``root``."""

    changed: list[Path] = []
    errors: list[tuple[Path, str]] = []
    for path in iter_secondary_pages(root):
        relative = path.relative_to(root)
        try:
            original = path.read_bytes()
            updated, needs_update = inject_brand(original, canonical_url(relative))
            if not needs_update:
                continue
            changed.append(relative)
            if write:
                _atomic_write(path, updated)
        except (OSError, BrandInjectionError) as error:
            errors.append((relative, str(error)))
    return changed, errors


def self_test() -> None:
    """Exercise injection and idempotency using temporary byte strings only."""

    canonical = "https://3parusa.ru/turkey.html"
    original = b"<!doctype html><html><head><title>Tour</title></head><body>Text</body></html>"
    updated, changed = inject_brand(original, canonical)
    assert changed
    assert OG_TAG in updated
    assert TWITTER_TAG in updated
    assert _canonical_tag(canonical) in updated
    assert CSS_TAG in updated
    assert SCRIPT_TAG in updated
    assert updated.endswith(b"<body>Text</body></html>")

    repeated, changed_again = inject_brand(updated, canonical)
    assert not changed_again
    assert repeated == updated

    existing_metadata = (
        b"<html><head>"
        b'<meta property="og:image" content="https://cdn.example/existing.jpg">'
        b'<link rel="canonical" href="https://3parusa.ru/existing.html">'
        b"</head><body></body></html>"
    )
    preserved, preserved_changed = inject_brand(
        existing_metadata,
        "https://3parusa.ru/replacement.html",
    )
    assert preserved_changed
    assert b"https://cdn.example/existing.jpg" in preserved
    assert b"https://3parusa.ru/existing.html" in preserved
    assert BRAND_OG_URL.encode("ascii") not in preserved
    assert TWITTER_TAG not in preserved
    assert b"replacement.html" not in preserved

    crlf_document = b"<HTML>\r\n<HEAD>\r\n<title>X</title>\r\n</HEAD>\r\n<body></body></HTML>"
    crlf_updated, _ = inject_brand(crlf_document, "https://3parusa.ru/blog/example.html")
    assert b"\r\n" in crlf_updated
    assert b"\n" not in crlf_updated.replace(b"\r\n", b"")

    partial = b"<html><head>" + CSS_TAG + b"</head><body></body></html>"
    partial_updated, _ = inject_brand(partial, canonical)
    assert partial_updated.count(CSS_TAG) == 1
    assert partial_updated.count(SCRIPT_TAG) == 1

    try:
        inject_brand(b"<html><body>No head close</body></html>", canonical)
    except BrandInjectionError:
        pass
    else:
        raise AssertionError("documents without </head> must fail safely")

    assert canonical_url(Path("blog/index.html")) == "https://3parusa.ru/blog/"
    assert canonical_url(Path("faq.html")) == "https://3parusa.ru/faq.html"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="atomically update matching HTML files")
    mode.add_argument(
        "--check",
        action="store_true",
        help="return a non-zero status when files still need updates",
    )
    mode.add_argument(
        "--self-test",
        action="store_true",
        help="run in-memory unit checks and do not inspect project HTML",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="site repository root (defaults to this script's parent repository)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.self_test:
        self_test()
        print("apply_brand.py self-test: OK (in-memory strings only)")
        return 0

    root = args.root.resolve()
    if not root.is_dir():
        print(f"error: site root does not exist: {root}", file=sys.stderr)
        return 2

    changed, errors = process_pages(root, write=args.write)
    action = "Updated" if args.write else "Would update"
    for relative in changed:
        print(f"{action}: {relative.as_posix()}")
    for relative, message in errors:
        print(f"Error: {relative.as_posix()}: {message}", file=sys.stderr)

    print(
        f"{action} {len(changed)} secondary page(s); "
        f"{len(errors)} error(s)."
    )
    if errors:
        return 2
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
