"""Post-generation hook for the pypackage template.

Runs inside the newly generated project directory. Handles docs, GitHub/Codeberg repo creation, uv.lock generation,
git initialisation, branch protection, and PyPI trusted-publisher setup.
"""

import json
import os
import pathlib
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

_shared_hooks = pathlib.Path("{{ cookiecutter._template }}").parent / "_shared" / "hooks"
sys.path.insert(0, str(_shared_hooks))
print(_shared_hooks)
from hook_utils import (  # noqa
    configure_branch_protection,  # noqa
    create_github_repo,  # noqa
    enable_github_pages,  # noqa
    generate_uv_lock,  # noqa
    preflight_github,  # noqa
    run,  # noqa
    select_license,  # noqa
)

OWNER = "{{ cookiecutter.repo_owner }}"
REPO = "{{ cookiecutter.package_name }}"
IMPORT_NAME = "{{ cookiecutter.import_name }}"
FIRST_VERSION = "{{ cookiecutter.first_version }}"
PUBLISH_TO_PYPI = "{{ cookiecutter.publish_to_pypi }}"
DOCS_TYPE = "{{ cookiecutter.docs_type }}"
GIT_FLOW = "{{ cookiecutter.git_flow }}"
GIT_HOSTING = "{{ cookiecutter.git_hosting }}"
DESCRIPTION = "{{ cookiecutter.project_short_description | replace('\"', '\\\"') }}"


def _build_commit_message() -> str:
    """Build the initial commit message listing every generated file or directory.

    Returns:
        Multi-line commit message string tailored to the chosen hosting, docs type, and PyPI publishing options.
    """
    lines = [
        "Initial scaffold from NERC-CEH/fdri-cookiecutter-pypackage",
        "",
        f"- src/{IMPORT_NAME}/ package with __init__, __main__",
        f"- tests/test_{IMPORT_NAME}.py",
    ]

    if DOCS_TYPE == "sphinx":
        lines.append("- docs/ with Sphinx configuration and Shibuya theme")
    else:
        lines.append("- docs/ placeholder")

    if GIT_HOSTING == "github":
        ci_extras = ", docs build and deploy" if DOCS_TYPE == "sphinx" else ""
        lines.append(f"- .github/workflows/pipeline.yml (CI{ci_extras})")

    if PUBLISH_TO_PYPI == "yes" and GIT_HOSTING == "github":
        lines.append("- .github/workflows/publish.yml (PyPI trusted publishing)")

    lines += [
        "- Makefile with development tasks",
        "- scripts/bump.py, scripts/release.py",
        "- pyproject.toml, uv.lock",
        f"- CHANGELOG/{FIRST_VERSION}.md",
        "- LICENSE",
        "- CITATION.cff",
        "- README.md, CONTRIBUTING.md",
        "- .editorconfig, .gitignore, .githooks/pre-commit",
    ]

    return "\n".join(lines)


def create_pypi_environment() -> None:
    """Create a 'pypi' GitHub Actions environment for trusted PyPI publishing."""
    if not shutil.which("gh"):
        print("  gh CLI not found, skipping pypi environment setup.")
        print("  Create manually: Settings > Environments > New environment > pypi")
        return

    result = run("gh", "api", f"repos/{OWNER}/{REPO}/environments/pypi", "-X", "PUT")
    if result.returncode == 0:
        print(f"  GitHub environment 'pypi' created for {OWNER}/{REPO}")
    else:
        print("  Could not create pypi environment automatically.")
        print("  Create manually: Settings > Environments > New environment > pypi")


def _codeberg_api(path: str, method: str = "GET", payload: dict | None = None) -> tuple[int, dict]:
    """Make an authenticated Codeberg Forgejo API call.

    Args:
        path: API path relative to ``/api/v1`` (e.g. ``"/user"``).
        method: HTTP method.
        payload: JSON-serialisable request body, or ``None`` for no body.

    Returns:
        A ``(status_code, parsed_body)`` tuple. On HTTP errors the body is
        parsed from the error response if possible, otherwise an empty dict.
    """
    token = os.environ.get("CODEBERG_TOKEN", "")
    req = urllib.request.Request(
        f"https://codeberg.org/api/v1{path}",
        data=json.dumps(payload).encode() if payload is not None else None,
        method=method,
    )
    req.add_header("Authorization", f"token {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body: dict = {}
        try:
            body = json.loads(e.read())
        except (json.JSONDecodeError, ValueError):
            pass
        return e.code, body


def preflight_codeberg() -> str | None:
    """Check that CODEBERG_TOKEN is set and valid.

    Returns:
        The authenticated Codeberg username on success, or ``None`` to skip all Codeberg API steps.
    """
    if not os.environ.get("CODEBERG_TOKEN"):
        print("  CODEBERG_TOKEN not set - skipping automatic repo creation.")
        print("  Set it to auto-create the repo (see docs/usage-codeberg.md).")
        return None

    status, body = _codeberg_api("/user")
    if status != 200:
        print(f"  CODEBERG_TOKEN check failed (HTTP {status}) - skipping automatic repo creation.")
        return None

    username = body.get("login", "")
    print(f"  Codeberg token valid (logged in as '{username}')")
    return username


def create_codeberg_repo(current_user: str) -> bool:
    """Create the Codeberg repo via the Forgejo API.

    Args:
        current_user: Authenticated Codeberg username.

    Returns:
        True if the repo was created or already existed, False on failure.
    """
    if not os.isatty(0):
        private = False
    else:
        choice = input("  Make the Codeberg repo public or private? [public/private] (public): ").strip().lower()
        private = choice == "private"

    endpoint = f"/orgs/{OWNER}/repos" if OWNER.lower() != current_user.lower() else "/user/repos"
    status, body = _codeberg_api(
        endpoint,
        method="POST",
        payload={
            "name": REPO,
            "description": DESCRIPTION,
            "private": private,
            "auto_init": False,
        },
    )

    if status in (200, 201):
        visibility = "private" if private else "public"
        print(f"  Codeberg repo created ({visibility}): https://codeberg.org/{OWNER}/{REPO}")
        return True
    elif status == 409 or "already exist" in str(body).lower():
        print(f"  Codeberg repo {OWNER}/{REPO} already exists")
        return True
    else:
        print(f"  Could not create repo (HTTP {status}): {body.get('message', str(body))}")
        print("  Create manually: https://codeberg.org/repo/create")
        return False


def git_init_and_push(
    repo_created: bool,
    remote_url: str | None = None,
    clean_url_override: str | None = None,
) -> None:
    """Initialise git, make the initial commit, and push to origin if a remote repo was created.

    Args:
        repo_created: Whether a remote repo exists to push to.
        remote_url: Push URL to use.
        clean_url_override: After a successful push the remote is reset to this URL (i.e. strips embedded tokens).
            Pass ``None`` to skip the reset, e.g. when the caller will push the develop branch next and will handle
            the reset itself.
    """
    try:
        subprocess.run(["git", "init", "-b", "main"], capture_output=True, check=True)
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], capture_output=True, check=True)
        subprocess.run(["git", "add", "."], capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", _build_commit_message()], capture_output=True, check=True)
        print("  Git initialized with initial commit")
        print("  Git hooks configured (.githooks/)")
    except subprocess.CalledProcessError:
        print("  Could not initialize git repo.")
        return

    if not repo_created:
        return

    if GIT_HOSTING == "github":
        push_url = f"https://github.com/{OWNER}/{REPO}.git"
        clean_url = push_url
        run("gh", "auth", "setup-git")
    else:
        clean_url = f"https://codeberg.org/{OWNER}/{REPO}.git"
        push_url = remote_url or clean_url

    try:
        subprocess.run(["git", "remote", "add", "origin", push_url], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print(f"  Could not add remote. Run: git remote add origin {clean_url} && git push -u origin main")
        return

    result = run("git", "push", "-u", "origin", "main")
    if result.returncode == 0:
        reset_url = clean_url_override if clean_url_override is not None else clean_url
        if push_url != reset_url:
            run("git", "remote", "set-url", "origin", reset_url)
        print(f"  Pushed to {clean_url.removesuffix('.git')}")
    else:
        print(f"  Could not push: {result.stderr.strip()}")
        print(f"  Run: git remote add origin {clean_url} && git push -u origin main")


def setup_develop_branch(repo_created: bool, auth_url: str | None = None) -> None:
    """Create a develop branch, push it, and set it as the default branch.

    Args:
        repo_created: Whether a remote repo exists to push to.
        auth_url: Token-embedded remote URL for the push (Codeberg only). The remote is reset to the clean HTTPS URL
            after pushing.
    """
    try:
        subprocess.run(["git", "checkout", "-b", "develop"], capture_output=True, check=True)
        print("  Created develop branch")
    except subprocess.CalledProcessError:
        print("  Could not create develop branch.")
        return

    if not repo_created:
        return

    if auth_url:
        run("git", "remote", "set-url", "origin", auth_url)

    result = run("git", "push", "-u", "origin", "develop")

    if auth_url:
        run("git", "remote", "set-url", "origin", f"https://codeberg.org/{OWNER}/{REPO}.git")

    if result.returncode != 0:
        print(f"  Could not push develop branch: {result.stderr.strip()}")
        return
    print("  Pushed develop branch to origin")

    if GIT_HOSTING == "github":
        result = run("gh", "api", "-X", "PATCH", f"repos/{OWNER}/{REPO}", "-f", "default_branch=develop")
        if result.returncode == 0:
            print("  GitHub default branch set to develop")
        else:
            print("  Could not set default branch.")
            print("  Set manually: Settings > General > Default branch")
    else:
        status, _ = _codeberg_api(f"/repos/{OWNER}/{REPO}", method="PATCH", payload={"default_branch": "develop"})
        if status == 200:
            print("  Codeberg default branch set to develop")
        else:
            print("  Could not set default branch.")
            print(f"  Set manually: https://codeberg.org/{OWNER}/{REPO}/settings (Branches)")


def print_codeberg_instructions() -> None:
    """Print manual steps for publishing to Codeberg when automatic setup was skipped."""
    print()
    print("  Your project has been created locally. To publish it on Codeberg:")
    print()
    print("  1. Create the repository at https://codeberg.org/repo/create")
    print(f"     Name:  {REPO}")
    print(f"     Owner: {OWNER}")
    print()
    print("  2. Add the remote and push:")
    print(f"     git remote add origin https://codeberg.org/{OWNER}/{REPO}.git")
    print("     git push -u origin main")
    if GIT_FLOW == "main_develop":
        print("     git push -u origin develop")
        print()
        print("  3. Set 'develop' as the default branch in:")
        print(f"     https://codeberg.org/{OWNER}/{REPO}/settings  (Branches section)")
    print()
    print("  To release a new version, see docs/releasing.md or run `make release` from main.")
    print()


def print_pypi_trusted_publisher_instructions() -> None:
    """Print the PyPI trusted publisher setup steps needed before the first release."""
    print()
    print("  To publish to PyPI, add a pending publisher at:")
    print("  https://pypi.org/manage/account/publishing/")
    print()
    print("  Fill in these values:")
    print(f"    PyPI project name:  {REPO}")
    print(f"    Owner:              {OWNER}")
    print(f"    Repository:         {REPO}")
    print("    Workflow:           publish.yml")
    print("    Environment:        pypi")
    print()
    print("  Then release with:")
    print("    make release")
    print()


if __name__ == "__main__":
    select_license("{{ cookiecutter.license }}")

    if DOCS_TYPE == "simple":
        shutil.rmtree("docs", ignore_errors=True)
        os.makedirs("docs")
        with open("docs/index.md", "w") as f:
            f.write(f"# {REPO}\n\nAdd your documentation here.\n")

    if GIT_HOSTING == "codeberg":
        shutil.rmtree(".github", ignore_errors=True)

        CODEBERG_USER = preflight_codeberg()
        REPO_CREATED = CODEBERG_USER is not None and create_codeberg_repo(CODEBERG_USER)

        TOKEN = os.environ.get("CODEBERG_TOKEN", "")
        AUTH_URL = f"https://oauth2:{TOKEN}@codeberg.org/{OWNER}/{REPO}.git" if REPO_CREATED else None
        SKIP_RESET = GIT_FLOW == "main_develop"

        generate_uv_lock()
        git_init_and_push(REPO_CREATED, remote_url=AUTH_URL, clean_url_override=AUTH_URL if SKIP_RESET else None)

        if GIT_FLOW == "main_develop":
            setup_develop_branch(REPO_CREATED, auth_url=AUTH_URL)

        if not REPO_CREATED:
            print_codeberg_instructions()

    elif GIT_HOSTING == "none":
        shutil.rmtree(".github", ignore_errors=True)

        generate_uv_lock()
        git_init_and_push(False)

        if GIT_FLOW == "main_develop":
            setup_develop_branch(False)

        print()
        print("  Local git repository initialised. No remote configured.")
        print("  When you're ready to publish, add a remote:")
        print("    git remote add origin <url>")
        print("    git push -u origin main")
        if GIT_FLOW == "main_develop":
            print("    git push -u origin develop")
        print()

    else:  # github
        if PUBLISH_TO_PYPI != "yes":
            publish_yml = os.path.join(".github", "workflows", "publish.yml")
            if os.path.exists(publish_yml):
                os.remove(publish_yml)

        REPO_CREATED = False
        if preflight_github(OWNER, REPO, warn_branch_protection=GIT_FLOW in ("github_flow", "main_develop")):
            REPO_CREATED = create_github_repo(OWNER, REPO, DESCRIPTION, default_visibility="public")
            if REPO_CREATED:
                if DOCS_TYPE == "sphinx":
                    enable_github_pages(OWNER, REPO)
                if PUBLISH_TO_PYPI == "yes":
                    create_pypi_environment()

        generate_uv_lock()
        git_init_and_push(REPO_CREATED)

        if GIT_FLOW == "main_develop":
            setup_develop_branch(REPO_CREATED)

        if REPO_CREATED and GIT_FLOW in ("github_flow", "main_develop"):
            contexts = ["test-python"]
            if DOCS_TYPE == "sphinx":
                contexts.append("build-docs")
            configure_branch_protection(OWNER, REPO, "main", contexts)
            if GIT_FLOW == "main_develop":
                configure_branch_protection(OWNER, REPO, "develop", contexts)

        if PUBLISH_TO_PYPI == "yes":
            print_pypi_trusted_publisher_instructions()

    print("Your Python package project has been created successfully!")
