"""Bake tests for the pyservice template."""

import os

PYSERVICE = os.path.abspath("pyservice")


def test_bake_with_defaults(cookies):
    result = cookies.bake(template=PYSERVICE)
    assert result.exit_code == 0, result.exception
    assert result.project_path.is_dir()


def test_has_dockerfile(cookies):
    result = cookies.bake(template=PYSERVICE)
    assert (result.project_path / "Dockerfile").exists()


def test_has_src_and_tests(cookies):
    result = cookies.bake(template=PYSERVICE)
    names = [f.name for f in result.project_path.iterdir()]
    assert "src" in names
    assert "tests" in names


def test_no_release_script(cookies):
    """release.py is pypackage-only."""
    result = cookies.bake(template=PYSERVICE)
    assert not (result.project_path / "scripts" / "release.py").exists()


def test_no_publish_workflow(cookies):
    """publish.yml is pypackage-only."""
    result = cookies.bake(template=PYSERVICE)
    assert not (result.project_path / ".github" / "workflows" / "publish.yml").exists()


def test_shared_contributing_git_flow(cookies):
    """Shared CONTRIBUTING.md renders the staging/production git flow for pyservice."""
    result = cookies.bake(template=PYSERVICE)
    assert result.exit_code == 0
    contributing = (result.project_path / "CONTRIBUTING.md").read_text()
    assert "off `staging`" in contributing


def test_pipeline_has_docker_jobs(cookies):
    """pyservice pipeline includes Docker build/deploy jobs."""
    result = cookies.bake(template=PYSERVICE)
    assert result.exit_code == 0
    pipeline = (result.project_path / ".github" / "workflows" / "pipeline.yml").read_text()
    assert "build-test-deploy-docker" in pipeline


def test_pipeline_import_name_substituted(cookies):
    """pyservice pipeline renders import_name correctly."""
    result = cookies.bake(
        template=PYSERVICE,
        extra_context={"package_name": "my-service"},
    )
    assert result.exit_code == 0
    pipeline = (result.project_path / ".github" / "workflows" / "pipeline.yml").read_text()
    assert "my_service" in pipeline
    assert "cookiecutter" not in pipeline


def test_shared_pyproject_renders(cookies):
    """Shared pyproject.toml has package name substituted correctly."""
    result = cookies.bake(
        template=PYSERVICE,
        extra_context={"package_name": "my-service", "first_version": "0.2.0"},
    )
    assert result.exit_code == 0
    content = (result.project_path / "pyproject.toml").read_text()
    assert 'name = "my-service"' in content
    assert 'version = "0.2.0"' in content
