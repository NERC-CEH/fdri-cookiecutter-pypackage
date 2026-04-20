"""Tests for README content rendering."""


def test_readme_contains_project_name(cookies):
    """Project name appears as the README title."""
    result = cookies.bake(extra_context={"project_name": "My Cool Package"})
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()
    assert "# My Cool Package" in readme


def test_readme_contains_description(cookies):
    """Project short description appears in README."""
    result = cookies.bake(extra_context={"project_short_description": "Does something useful"})
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()
    assert "Does something useful" in readme


def test_readme_contains_github_link(cookies):
    """GitHub repo link appears in README for github hosting."""
    result = cookies.bake(
        extra_context={
            "package_name": "my-package",
            "repo_owner": "NERC-CEH",
            "git_hosting": "github",
        }
    )
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()
    assert "https://github.com/NERC-CEH/my-package" in readme


def test_readme_contains_codeberg_link(cookies):
    """Codeberg repo link appears in README for codeberg hosting."""
    result = cookies.bake(
        extra_context={
            "package_name": "my-package",
            "repo_owner": "NERC-CEH",
            "git_hosting": "codeberg",
        }
    )
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()
    assert "https://codeberg.org/NERC-CEH/my-package" in readme


def test_readme_references_fdri_template(cookies):
    """README credits the FDRI cookiecutter template."""
    result = cookies.bake()
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()
    assert "NERC-CEH/fdri-cookiecutter-pypackage" in readme


def test_readme_sphinx_docs_section_present_for_sphinx(cookies):
    """README includes docs section when docs_type is sphinx."""
    result = cookies.bake(extra_context={"docs_type": "sphinx"})
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()
    assert "make docs-serve" in readme


def test_readme_sphinx_docs_section_absent_for_simple(cookies):
    """README does not include Sphinx docs commands when docs_type is simple."""
    result = cookies.bake(extra_context={"docs_type": "simple"})
    assert result.exit_code == 0
    readme = (result.project_path / "README.md").read_text()
    assert "make docs-serve" not in readme
