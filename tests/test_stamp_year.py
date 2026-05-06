"""Unit tests for hook_utils.stamp_year."""

import pathlib
import sys
from datetime import datetime

import pytest

REPO = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO / "_shared" / "hooks"))

from hook_utils import stamp_year  # noqa: E402


@pytest.fixture()
def tmp_project(tmp_path):
    """Change into a temporary directory and yield it, restoring cwd afterwards."""
    original = pathlib.Path.cwd()
    import os

    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original)


def test_stamp_year_replaces_placeholder(tmp_project):
    """COOKIECUTTER_YEAR is replaced with the current year."""
    f = tmp_project / "LICENSE"
    f.write_text("Copyright (c) COOKIECUTTER_YEAR Some Author")
    stamp_year()
    assert str(datetime.now().year) in f.read_text()
    assert "COOKIECUTTER_YEAR" not in f.read_text()


def test_stamp_year_replaces_in_all_files(tmp_project):
    """Placeholder is replaced across multiple files and subdirectories."""
    (tmp_project / "docs").mkdir()
    files = [
        tmp_project / "LICENSE",
        tmp_project / "docs" / "conf.py",
    ]
    for f in files:
        f.write_text("year: COOKIECUTTER_YEAR")
    stamp_year()
    year = str(datetime.now().year)
    for f in files:
        assert year in f.read_text()
        assert "COOKIECUTTER_YEAR" not in f.read_text()


def test_stamp_year_skips_binary_files(tmp_project):
    """Binary files that cannot be decoded as UTF-8 are silently skipped."""
    binary = tmp_project / "image.png"
    binary.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")
    stamp_year()  # should not raise


def test_stamp_year_no_placeholder_is_noop(tmp_project):
    """Files without the placeholder are left unchanged."""
    f = tmp_project / "README.md"
    original = "No placeholder here."
    f.write_text(original)
    stamp_year()
    assert f.read_text() == original
