"""Post-generation hook for the pyservice template.

Runs inside the newly generated project directory. Handles docs, GitHub repo creation, uv.lock generation,
git initialisation across the staging/production branches, branch protection, and AWS secrets guidance.
"""

import os
import pathlib
import shutil
import subprocess
import sys

TEMPLATE = pathlib.Path("{{ cookiecutter._template }}")
SHARED_HOOKS = TEMPLATE / "_shared" / "hooks"
if not SHARED_HOOKS.exists():
    SHARED_HOOKS = TEMPLATE.parent / "_shared" / "hooks"
sys.path.insert(0, str(SHARED_HOOKS))

from hook_utils import (  # noqa
    configure_branch_protection,  # noqa
    create_github_repo,  # noqa
    enable_github_pages,  # noqa
    generate_uv_lock,  # noqa
    preflight_github,  # noqa
    run,  # noqa
    select_license,  # noqa
    stamp_year,  # noqa
)

OWNER = "{{ cookiecutter.repo_owner }}"
REPO = "{{ cookiecutter.package_name }}"
IMPORT_NAME = "{{ cookiecutter.import_name }}"
FIRST_VERSION = "{{ cookiecutter.first_version }}"
DOCS_TYPE = "{{ cookiecutter.docs_type }}"
DESCRIPTION = "{{ cookiecutter.project_short_description | replace('\"', '\\\"') }}"

BRANCHES = ["staging", "production"]


def _build_commit_message() -> str:
    """Build the initial commit message listing every generated file or directory.

    Returns:
        Multi-line commit message string tailored to the chosen docs type.
    """
    lines = [
        "Initial scaffold from NERC-CEH/fdri-cookiecutter (pyservice)",
        "",
        f"- src/{IMPORT_NAME}/ package with __init__, __main__",
        f"- tests/test_{IMPORT_NAME}.py",
        "- Dockerfile (uv-based multi-stage)",
        "- .github/workflows/pipeline.yml (test + build/deploy docker, auto-PR staging->production)",
    ]
    if DOCS_TYPE == "sphinx":
        lines.append("- docs/ with Sphinx configuration and Shibuya theme")
    else:
        lines.append("- docs/ placeholder")
    lines += [
        "- Makefile with development tasks",
        "- scripts/bump.py",
        "- pyproject.toml, uv.lock",
        f"- CHANGELOG/{FIRST_VERSION}.md",
        "- LICENSE",
        "- CITATION.cff",
        "- README.md, CONTRIBUTING.md",
        "- .editorconfig, .gitignore, .githooks/pre-commit",
    ]
    return "\n".join(lines)


def git_init_and_push_all_branches(repo_created: bool) -> None:
    """Initialise git, commit, and push both environment branches.

    Creates staging (default) and production branches. Pushes both to origin if a remote repo was created.

    Args:
        repo_created: Whether a remote repo exists to push to.
    """
    try:
        subprocess.run(["git", "init", "-b", "staging"], capture_output=True, check=True)
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], capture_output=True, check=True)
        subprocess.run(["git", "add", "."], capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", _build_commit_message()], capture_output=True, check=True)
        print("  Git initialized with initial commit")
    except subprocess.CalledProcessError:
        print("  Could not initialize git repo.")
        return

    try:
        subprocess.run(["git", "branch", "production"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("  Could not create production branch.")
        return
    print("  Created staging and production branches")

    if not repo_created:
        return

    run("gh", "auth", "setup-git")
    push_url = f"https://github.com/{OWNER}/{REPO}.git"
    try:
        subprocess.run(["git", "remote", "add", "origin", push_url], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print(f"  Could not add remote. Run: git remote add origin {push_url}")
        return

    for branch in BRANCHES:
        result = run("git", "push", "-u", "origin", branch)
        if result.returncode == 0:
            print(f"  Pushed {branch} to origin")
        else:
            print(f"  Could not push {branch}: {result.stderr.strip()}")


def print_secrets_instructions() -> None:
    """Print the AWS OIDC secrets that must be added before the first deploy."""
    print()
    print("  REQUIRED: Add these repository secrets before the first deploy:")
    print(f"    https://github.com/{OWNER}/{REPO}/settings/secrets/actions")
    print()
    print("    AWS_REGION                 (e.g. eu-west-2)")
    print("    AWS_ROLE_ARN_STAGING       (OIDC role in the staging AWS account)")
    print("    AWS_ROLE_ARN_PRODUCTION    (OIDC role in the production AWS account)")
    print()
    print("  See docs for more info, or ask an FDRI admin.")
    print()


if __name__ == "__main__":
    stamp_year()
    select_license("{{ cookiecutter.license }}")

    if DOCS_TYPE == "simple":
        shutil.rmtree("docs", ignore_errors=True)
        os.makedirs("docs")
        with open("docs/index.md", "w") as f:
            f.write(f"# {REPO}\n\nAdd your documentation here.\n")

    REPO_CREATED = False
    if preflight_github(OWNER, REPO, warn_branch_protection=True):
        REPO_CREATED = create_github_repo(OWNER, REPO, DESCRIPTION, default_visibility="private")
        if REPO_CREATED:
            if DOCS_TYPE == "sphinx":
                enable_github_pages(OWNER, REPO)

    generate_uv_lock()
    git_init_and_push_all_branches(REPO_CREATED)

    if REPO_CREATED:
        CONTEXTS = ["test-python"]
        if DOCS_TYPE == "sphinx":
            CONTEXTS.append("build-docs")
        for BRANCH in BRANCHES:
            configure_branch_protection(OWNER, REPO, BRANCH, CONTEXTS)

    print_secrets_instructions()
    print("Your Python service project has been created successfully!")
