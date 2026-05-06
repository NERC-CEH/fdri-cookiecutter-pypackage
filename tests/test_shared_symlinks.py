"""Verify every file in _shared/ has a corresponding symlink in each template."""

import pathlib

import pytest

REPO = pathlib.Path(__file__).parent.parent
SHARED_ROOT = REPO / "_shared" / "{{cookiecutter.package_name}}"
TEMPLATES = ["pypackage", "pyservice"]


def shared_files():
    return [f.relative_to(SHARED_ROOT) for f in SHARED_ROOT.rglob("*") if f.is_file()]


@pytest.mark.parametrize("template", TEMPLATES)
@pytest.mark.parametrize("rel", shared_files(), ids=str)
def test_symlink_exists(template, rel):
    link = REPO / template / "{{cookiecutter.package_name}}" / rel
    assert link.is_symlink(), f"{link} is not a symlink"
    assert link.exists(), f"{link} is a broken symlink"
