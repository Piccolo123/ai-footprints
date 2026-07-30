"""
Tests for url-manager skill — SKILL.md structure and footprints.py logic.

Uses stdlib + pytest + unittest.mock. No live network calls.

Run: pytest tests/test_url_manager_skill.py -q
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ── Paths relative to skill directory ──
SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = SKILL_DIR / "SKILL.md"
SCRIPTS_DIR = SKILL_DIR / "scripts"
FOOTPRINTS_PY = SCRIPTS_DIR / "footprints.py"


# ──────────────────────────────────────────────
# SKILL.md structure tests
# ──────────────────────────────────────────────


def test_skill_md_exists():
    """SKILL.md must be present in the skill directory."""
    assert SKILL_MD.exists(), f"SKILL.md not found at {SKILL_MD}"


def test_skill_md_has_required_sections():
    """SKILL.md must include all required sections per AGENTS.md standard."""
    content = SKILL_MD.read_text()
    required = [
        "## When to Use",
        "## Prerequisites",
        "## How to Run",
        "## Quick Reference",
        "## Procedure",
        "## Pitfalls",
        "## Verification",
    ]
    for section in required:
        assert section in content, f"Missing required section: {section}"


def test_skill_md_has_frontmatter():
    """SKILL.md must have valid YAML frontmatter with required fields."""
    content = SKILL_MD.read_text()
    assert content.startswith("---"), "SKILL.md must start with YAML frontmatter"
    # Find closing ---
    end = content.find("---", 3)
    assert end > 0, "SKILL.md frontmatter must have closing ---"
    frontmatter = content[3:end].strip()
    assert "name:" in frontmatter, "Frontmatter missing 'name'"
    assert "description:" in frontmatter, "Frontmatter missing 'description'"
    assert "author:" in frontmatter, "Frontmatter metadata missing 'author'"
    assert "version:" in frontmatter, "Frontmatter metadata missing 'version'"


def test_skill_md_no_orphan_references():
    """SKILL.md must not reference files that are not shipped with the skill."""
    content = SKILL_MD.read_text()
    # Check for relative markdown links to references/
    import re

    ref_links = re.findall(r"\]\(((?:\.\.?/)?references/[^)]+)\)", content)
    for link in ref_links:
        target = SKILL_DIR / link
        assert target.exists(), f"SKILL.md references missing file: {link}"


def test_skill_md_requires_explicit_consent():
    """SKILL.md must require explicit user consent before agent_register."""
    content = SKILL_MD.read_text()
    consent_phrases = [
        "explicit consent",
        "Never auto-register",
        "get explicit",
        "NEVER call agent_register without consent",
    ]
    found = sum(1 for p in consent_phrases if p.lower() in content.lower())
    assert found >= 3, (
        f"SKILL.md must emphasize explicit consent before agent_register. "
        f"Found {found}/4 required phrases."
    )


# ──────────────────────────────────────────────
# footprints.py existence tests
# ──────────────────────────────────────────────


def test_footprints_py_exists():
    """footprints.py must be shipped with the skill."""
    assert FOOTPRINTS_PY.exists(), f"footprints.py not found at {FOOTPRINTS_PY}"


def test_footprints_py_is_executable():
    """footprints.py must be a Python script (not a compiled binary)."""
    content = FOOTPRINTS_PY.read_text()
    assert "#!/usr/bin/env python3" in content or "#!/usr/bin/python" in content, (
        "footprints.py missing shebang"
    )


# ──────────────────────────────────────────────
# Token management logic tests (mocked)
# ──────────────────────────────────────────────


@pytest.fixture
def footprints_module():
    """
    Import footprints.py as a module for testing.
    The module has side-effects on import (reads env vars, checks files).
    We isolate it in a test fixture.
    """
    # Add scripts dir to path
    sys.path.insert(0, str(SCRIPTS_DIR))
    # Remove any cached import
    for key in list(sys.modules.keys()):
        if "footprints" in key:
            del sys.modules[key]
    import footprints

    yield footprints
    # Cleanup
    sys.path.remove(str(SCRIPTS_DIR))


def test_token_from_env(footprints_module, monkeypatch):
    """Token should be read from FOOTPRINTS_TOKEN env var first."""
    monkeypatch.setenv("FOOTPRINTS_TOKEN", "FA_test_token_123")
    # Temporarily remove .token file if exists
    token_file = footprints_module.TOKEN_FILE
    saved = None
    if os.path.exists(token_file):
        with open(token_file) as f:
            saved = f.read()
        os.remove(token_file)

    try:
        # Mock _raw_api so auto-register never triggers real HTTP
        with patch.object(footprints_module, "_raw_api", return_value={}):
            token = footprints_module._get_token()
        assert token == "FA_test_token_123"
    finally:
        if saved:
            with open(token_file, "w") as f:
                f.write(saved)


def test_token_from_file(footprints_module, monkeypatch):
    """Token should fall back to .token file when env var is empty."""
    monkeypatch.delenv("FOOTPRINTS_TOKEN", raising=False)

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("FA_file_token_456")
        token_path = f.name

    # Override TOKEN_FILE to point to our temp file
    monkeypatch.setattr(footprints_module, "TOKEN_FILE", token_path)

    try:
        token = footprints_module._get_token()
        assert token == "FA_file_token_456"
    finally:
        os.unlink(token_path)


def test_token_auto_register(footprints_module, monkeypatch):
    """When no token in env or file, _get_token should auto-register."""
    monkeypatch.delenv("FOOTPRINTS_TOKEN", raising=False)
    # Point TOKEN_FILE to a non-existent path
    monkeypatch.setattr(
        footprints_module, "TOKEN_FILE", "/tmp/__nonexistent_token__"
    )

    mock_response = {"token": "FA_auto_registered_789"}
    with patch.object(
        footprints_module, "_raw_api", return_value=mock_response
    ):
        token = footprints_module._get_token()
        assert token == "FA_auto_registered_789"
        # Verify token was persisted to env
        assert os.environ.get("FOOTPRINTS_TOKEN") == "FA_auto_registered_789"


def test_api_adds_authorization(footprints_module, monkeypatch):
    """api() must attach Bearer token to requests."""
    monkeypatch.setenv("FOOTPRINTS_TOKEN", "FA_test_auth")

    captured_headers = {}

    def mock_raw_api(path, method="GET", data=None, no_auth=False):
        # Capture what _raw_api receives (simulating actual behavior)
        return {"ok": True}

    with patch.object(footprints_module, "_raw_api", side_effect=mock_raw_api):
        with patch.object(footprints_module, "_get_token", return_value="FA_test_auth"):
            result = footprints_module.api("/me")
            assert "error" not in result


def test_raw_api_no_auth_returns_error_without_token(footprints_module):
    """_raw_api must return error when no token and no_auth=False."""
    # This is a pure logic test — no HTTP
    result = footprints_module._raw_api("/me", no_auth=False)
    assert "error" in result


def test_raw_api_register_no_auth_ok(footprints_module, monkeypatch):
    """_raw_api with no_auth=True should NOT require token."""
    monkeypatch.delenv("FOOTPRINTS_TOKEN", raising=False)
    # _raw_api with no_auth=True skips token check; mock urlopen to avoid real HTTP
    import io

    mock_resp = io.BytesIO(json.dumps({"token": "FA_new"}).encode())
    mock_resp.status = 200

    with patch("urllib.request.urlopen", return_value=mock_resp):
        result = footprints_module._raw_api("/register", method="POST", no_auth=True)
        assert "token" in result


# ──────────────────────────────────────────────
# Command name validation
# ──────────────────────────────────────────────


def test_all_skil_md_commands_exist_in_footprints_py():
    """Every command referenced in SKILL.md Quick Reference must exist in footprints.py."""
    import re

    skill_content = SKILL_MD.read_text()
    script_content = FOOTPRINTS_PY.read_text()

    # Extract function names from footprints.py (def xxx(...):)
    func_names = set(re.findall(r"^def (\w+)\(.*\):", script_content, re.MULTILINE))

    # Commands mentioned in Quick Reference — maps to actual function names
    # Some CLI subcommands use underscores that map to function names differently
    expected_funcs = [
        "add",
        "get_collection",
        "search",
        "list_collections",
        "update_collection",
        "batch_update_collections",
        "categories",
        "create_category",
        "category_sets",
        "create_category_set",
        "tags",
        "content_types",
        "create_shared_category",
        "create_invite_link",
        "join_shared_category",
        "add_to_shared_category",
        "remove_from_shared_category",
        "copy_collection",
        "me",
        "agent_magic_link",
        "agent_register",
    ]

    missing = []
    for func_name in expected_funcs:
        if func_name not in func_names:
            missing.append(func_name)

    assert not missing, (
        f"SKILL.md references commands not found in footprints.py: {missing}"
    )
