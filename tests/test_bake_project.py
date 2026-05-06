"""Bake tests for the pypackage template.

Covers default generation, special characters in author names and descriptions,
git-flow variants, ruff/pytest passing out of the box, and pypackage-specific
files that must not appear in pyservice projects.
"""

import shlex
import subprocess
import sys

import pytest


def run_inside_dir(command: str, dirpath: str) -> int:
    """Run a shell command inside a generated project directory.

    Args:
        command: Shell command string to execute.
        dirpath: Working directory for the command.

    Returns:
        Zero on success; raises ``subprocess.CalledProcessError`` on failure.
    """
    return subprocess.check_call(shlex.split(command), cwd=dirpath)


def check_output_inside_dir(command: str, dirpath: str) -> bytes:
    """Capture stdout of a shell command run inside a generated project directory.

    Args:
        command: Shell command string to execute.
        dirpath: Working directory for the command.

    Returns:
        Raw stdout bytes.
    """
    return subprocess.check_output(shlex.split(command), cwd=dirpath)


def test_pypackage_specific_files(cookies):
    """Files that exist only in pypackage, not pyservice."""
    result = cookies.bake()
    assert result.exit_code == 0
    assert (result.project_path / "scripts" / "release.py").exists()
    assert not (result.project_path / "Dockerfile").exists()


def test_license_mit_default(cookies):
    result = cookies.bake()
    assert result.exit_code == 0
    license_file = result.project_path / "LICENSE"
    assert license_file.exists()
    assert "MIT License" in license_file.read_text()
    assert not (result.project_path / "LICENSE.MIT").exists()
    assert not (result.project_path / "LICENSE.GPL").exists()


def test_license_gpl_option(cookies):
    result = cookies.bake(extra_context={"license": "GNU GPL v3.0"})
    assert result.exit_code == 0
    license_file = result.project_path / "LICENSE"
    assert license_file.exists()
    assert "GNU GENERAL PUBLIC LICENSE" in license_file.read_text()
    assert not (result.project_path / "LICENSE.MIT").exists()
    assert not (result.project_path / "LICENSE.GPL").exists()


def test_bake_with_defaults(cookies):
    result = cookies.bake()
    assert result.exit_code == 0, result.exception
    assert result.project_path.is_dir()
    found_toplevel_files = [f.name for f in result.project_path.iterdir()]
    assert "src" in found_toplevel_files
    assert "tests" in found_toplevel_files


def test_bake_and_run_tests(cookies):
    result = cookies.bake()
    assert result.project_path.is_dir()
    run_inside_dir("uv run pytest", str(result.project_path))


@pytest.mark.parametrize("git_hosting", ["github", "codeberg", "none"])
def test_bake_and_run_ruff(cookies, git_hosting):
    """Baked project passes ruff linting and formatting out of the box."""
    result = cookies.bake(extra_context={"git_hosting": git_hosting})
    assert result.project_path.is_dir()
    run_inside_dir("uv run ruff check .", str(result.project_path))
    run_inside_dir("uv run ruff format --check --diff .", str(result.project_path))


@pytest.mark.parametrize(
    "full_name",
    [
        'name "quote" name',
        "O'connor",
    ],
)
def test_bake_special_full_name_and_run_tests(cookies, full_name):
    """Special characters in full_name must not break pyproject.toml."""
    result = cookies.bake(extra_context={"full_name": full_name})
    assert result.exit_code == 0, result.exception
    run_inside_dir("uv run pytest", str(result.project_path))


def test_bake_with_quotes_in_description(cookies):
    """Ensure that double quotes in project_short_description produce valid TOML."""
    result = cookies.bake(extra_context={"project_short_description": 'A "quoted" description'})
    assert result.exit_code == 0, result.exception
    content = (result.project_path / "pyproject.toml").read_text()
    assert 'description = "A \\"quoted\\" description"' in content


@pytest.mark.skipif(sys.platform == "win32", reason="Makefile not supported on Windows")
def test_make_help(cookies):
    result = cookies.bake()
    output = check_output_inside_dir("make help", str(result.project_path))
    assert b"qa" in output


@pytest.mark.parametrize("git_flow", ["simple", "github_flow", "main_develop"])
def test_bake_git_flow_pipeline_triggers(cookies, git_flow):
    result = cookies.bake(extra_context={"git_flow": git_flow})
    assert result.exit_code == 0
    pipeline_path = result.project_path / ".github" / "workflows" / "pipeline.yml"
    pipeline = pipeline_path.read_text()
    if git_flow == "main_develop":
        assert "- develop" in pipeline
    else:
        assert "- develop" not in pipeline


@pytest.mark.parametrize("git_flow", ["simple", "github_flow", "main_develop"])
def test_bake_git_flow_contributing(cookies, git_flow):
    result = cookies.bake(extra_context={"git_flow": git_flow})
    assert result.exit_code == 0
    contributing = (result.project_path / "CONTRIBUTING.md").read_text()
    if git_flow == "simple":
        assert "feature branches" not in contributing.lower()
    elif git_flow == "github_flow":
        assert "off `main`" in contributing
        assert "1 approving review" in contributing
    elif git_flow == "main_develop":
        assert "off `develop`" in contributing
        assert "release PR" in contributing
