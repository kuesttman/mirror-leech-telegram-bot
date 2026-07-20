"""Tests for torrent web file selection URL generation."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlsplit, urlunsplit


def _load_url_helper():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "bot"
        / "helper"
        / "ext_utils"
        / "bot_utils.py"
    )
    src = file_path.read_text(encoding="utf-8")
    namespace: dict[str, object] = {
        "Config": SimpleNamespace(BASE_URL="", BASE_URL_PORT=80),
        "urlsplit": urlsplit,
        "urlunsplit": urlunsplit,
    }
    snippet_start = src.find("def _web_selection_base_url(")
    snippet_end = src.find("\ndef bt_selection_buttons(", snippet_start + 1)
    snippet = src[snippet_start:snippet_end]
    exec(snippet, namespace)  # noqa: S102 - test-only controlled exec
    return namespace["_web_selection_base_url"]


def test_web_selection_url_adds_port_when_base_url_has_no_port():
    build_url = _load_url_helper()
    config = SimpleNamespace(BASE_URL="100.64.16.160", BASE_URL_PORT=9090)

    assert build_url(config) == "http://100.64.16.160:9090"


def test_web_selection_url_keeps_explicit_base_url_port():
    build_url = _load_url_helper()
    config = SimpleNamespace(BASE_URL="http://100.64.16.160:9090", BASE_URL_PORT=80)

    assert build_url(config) == "http://100.64.16.160:9090"
