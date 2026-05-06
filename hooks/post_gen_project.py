#!/usr/bin/env python
"""Post-generation hooks for fdri-cookiecutter-pypackage."""

import json
import os
import pathlib
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import datetime

OWNER = "{{ cookiecutter.repo_owner }}"
REPO = "{{ cookiecutter.package_name }}"
IMPORT_NAME = "{{ cookiecutter.import_name }}"
FIRST_VERSION = "{{ cookiecutter.first_version }}"
PUBLISH_TO_PYPI = "{{ cookiecutter.publish_to_pypi }}"
DOCS_TYPE = "{{ cookiecutter.docs_type }}"
GIT_FLOW = "{{ cookiecutter.git_flow }}"
GIT_HOSTING = "{{ cookiecutter.git_hosting }}"


def _run(*args, **kwargs):
    """Thin wrapper around subprocess.run with sensible defaults."""
    kwargs.setdefault("capture_output", True)
    kwargs.setdefault("text", True)
    kwargs.setdefault("check", False)
    return subprocess.run(args, **kwargs)


def stamp_year():
    """Replace the COOKIECUTTER_YEAR placeholder with the current year in all generated files."""
    year = str(datetime.now().year)
    for path in pathlib.Path(".").rglob("*"):
        if path.is_file():
            try:
                text = path.read_text()
                if "COOKIECUTTER_YEAR" in text:
                    path.write_text(text.replace("COOKIECUTTER_YEAR", year))
            except (UnicodeDecodeError, PermissionError):
                pass


def select_license(license_choice):
    """Rename the chosen license file to LICENSE and remove the unused alternatives."""
    license_files = {"MIT": "LICENSE.MIT", "GNU GPL v3.0": "LICENSE.GPL"}
    for name, filename in license_files.items():
        p = pathlib.Path(filename)
        if not p.exists():
            continue
        if name == license_choice:
            p.rename("LICENSE")
        else:
            p.unlink()


def _build_commit_message():
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


# ---------------------------------------------------------------------------
# GitHub
# ---------------------------------------------------------------------------


def preflight_github():
    """Verify gh CLI can perform every GitHub operation we need.

    Returns True if setup can proceed, False to skip all GitHub steps.
    Attempts to refresh a missing 'workflow' scope automatically.
    """
    if not shutil.which("gh"):
        print("  gh CLI not found - skipping GitHub setup.")
        print(f"  Create manually: https://github.com/new?name={REPO}&owner={OWNER}")
        return False

    if _run("gh", "auth", "status").returncode != 0:
        print("  gh is not authenticated - skipping GitHub setup.")
        print("  Run 'gh auth login' then re-run cookiecutter.")
        return False

    result = _run("gh", "api", "user", "--include")
    if result.returncode != 0:
        print(f"  gh api call failed - skipping GitHub setup: {result.stderr.strip()}")
        return False

    scopes = ""
    for line in result.stdout.splitlines():
        if line.lower().startswith("x-oauth-scopes:"):
            scopes = line.split(":", 1)[1].strip()
            break

    if "repo" not in scopes:
        print("  gh token lacks required 'repo' scope - skipping GitHub setup.")
        print("  Refresh with: gh auth refresh -s repo,workflow")
        return False

    if "workflow" not in scopes:
        if os.environ.get("GH_TOKEN"):
            print("  GH_TOKEN lacks 'workflow' scope - pushing CI workflows will fail.")
            print("  Regenerate token with 'workflow' scope at https://github.com/settings/tokens")
            return False
        print("  gh token missing 'workflow' scope - re-authorising (browser will open)...")
        _run("gh", "auth", "refresh", "-s", "workflow")

    current_user = _run("gh", "api", "user", "-q", ".login").stdout.strip()

    if current_user and current_user.lower() != OWNER.lower():
        org_check = _run("gh", "api", f"orgs/{OWNER}/memberships/{current_user}")
        if org_check.returncode != 0:
            print(f"  Logged in as '{current_user}' but no access to '{OWNER}' - skipping GitHub setup.")
            return False

    if GIT_FLOW in ("github_flow", "main_develop") and current_user and current_user.lower() == OWNER.lower():
        print("  Note: branch protection on private repos requires GitHub Pro for personal accounts.")

    return True


def create_github_repo():
    """Create the GitHub repo. Asks the user whether it should be public or private."""
    if not os.isatty(0):
        return False

    choice = input("  Make the GitHub repo public or private? [public/private] (public): ").strip().lower()
    visibility = "--private" if choice == "private" else "--public"

    result = _run(
        "gh",
        "repo",
        "create",
        f"{OWNER}/{REPO}",
        visibility,
        "--description",
        "{{ cookiecutter.project_short_description | replace('\"', '\\\"') }}",
    )
    if result.returncode == 0:
        print(f"  GitHub repo created: https://github.com/{OWNER}/{REPO}")
        return True
    elif "already exists" in result.stderr:
        print(f"  GitHub repo {OWNER}/{REPO} already exists")
        return True
    else:
        print(f"  Could not create repo: {result.stderr.strip()}")
        print(f"  Create manually: https://github.com/new?name={REPO}&owner={OWNER}")
        return False


def enable_github_pages():
    """Enable GitHub Pages with Actions source."""
    if not shutil.which("gh"):
        print("  gh CLI not found, skipping GitHub Pages setup.")
        print("  Enable manually: Settings > Pages > Source > GitHub Actions")
        return

    _run("gh", "api", f"repos/{OWNER}/{REPO}/pages", "-X", "POST", "-f", "build_type=workflow")
    _run("gh", "api", f"repos/{OWNER}/{REPO}/pages", "-X", "PUT", "-f", "build_type=workflow")
    print(f"  GitHub Pages enabled for {OWNER}/{REPO} (source: GitHub Actions)")


def create_pypi_environment():
    """Create a 'pypi' GitHub environment for trusted publishing."""
    if not shutil.which("gh"):
        print("  gh CLI not found, skipping pypi environment setup.")
        print("  Create manually: Settings > Environments > New environment > pypi")
        return

    result = _run("gh", "api", f"repos/{OWNER}/{REPO}/environments/pypi", "-X", "PUT")
    if result.returncode == 0:
        print(f"  GitHub environment 'pypi' created for {OWNER}/{REPO}")
    else:
        print("  Could not create pypi environment automatically.")
        print("  Create manually: Settings > Environments > New environment > pypi")


def configure_branch_protection(branch):
    """Apply branch protection rules via the GitHub API."""
    if not shutil.which("gh"):
        print(f"  gh CLI not found, skipping branch protection for {branch}.")
        print(f"  Enable manually: Settings > Branches > Add rule for '{branch}'")
        return

    contexts = ["test-python"]
    if DOCS_TYPE == "sphinx":
        contexts.append("build-docs")

    payload = {
        "required_status_checks": {"strict": True, "contexts": contexts},
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "dismiss_stale_reviews": False,
            "require_code_owner_reviews": False,
        },
        "required_conversation_resolution": True,
        "restrictions": None,
        "allow_force_pushes": False,
        "allow_deletions": False,
    }

    result = subprocess.run(
        ["gh", "api", "-X", "PUT", f"repos/{OWNER}/{REPO}/branches/{branch}/protection", "--input", "-"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        print(f"  Branch protection configured for '{branch}'")
    elif "403" in result.stderr or "Upgrade" in result.stderr:
        print(f"  Branch protection skipped for '{branch}': not available for private repos on free personal accounts.")
        print("  (Works for GitHub org repos, or upgrade to GitHub Pro.)")
    else:
        print(f"  Could not configure branch protection for '{branch}': {result.stderr.strip()}")
        print(f"  Enable manually: Settings > Branches > Add rule for '{branch}'")


# ---------------------------------------------------------------------------
# Codeberg
# ---------------------------------------------------------------------------


def _codeberg_api(path, method="GET", payload=None):
    """Make an authenticated Codeberg API call. Returns (status_code, parsed_body)."""
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
        body = {}
        try:
            body = json.loads(e.read())
        except Exception:
            pass
        return e.code, body


def preflight_codeberg():
    """Check CODEBERG_TOKEN is set and valid.

    Returns the authenticated username on success, False to skip Codeberg API steps.
    """
    if not os.environ.get("CODEBERG_TOKEN"):
        print("  CODEBERG_TOKEN not set - skipping automatic repo creation.")
        print("  Set it to auto-create the repo (see docs/usage-codeberg.md).")
        return False

    status, body = _codeberg_api("/user")
    if status != 200:
        print(f"  CODEBERG_TOKEN check failed (HTTP {status}) - skipping automatic repo creation.")
        return False

    username = body.get("login", "")
    print(f"  Codeberg token valid (logged in as '{username}')")
    return username


def create_codeberg_repo(current_user):
    """Create the Codeberg repo via the Forgejo API."""
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
            "description": "{{ cookiecutter.project_short_description | replace('\"', '\\\"') }}",
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


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------


def generate_uv_lock():
    """Generate uv.lock so CI's 'uv sync --locked' has something to pin to."""
    if not shutil.which("uv"):
        print("  uv not found - skipping uv.lock generation.")
        print("  Install uv and run 'uv lock' before pushing, or CI will fail.")
        return

    result = _run("uv", "lock")
    if result.returncode == 0:
        print("  Generated uv.lock")
    else:
        print(f"  'uv lock' failed: {result.stderr.strip()}")
        print("  Run 'uv lock' manually before pushing, or CI will fail.")


def git_init_and_push(repo_created, remote_url=None, clean_url_override=None):
    """Initialise git, make the initial commit, and push if a remote repo exists.

    remote_url: if provided, used as-is for the push (e.g. a token-embedded Codeberg URL).
    clean_url_override: if provided, the remote is reset to this URL after a successful push.
      Pass None to skip the reset (e.g. when the caller will handle it after a develop branch push).
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
        _run("gh", "auth", "setup-git")
    else:
        clean_url = f"https://codeberg.org/{OWNER}/{REPO}.git"
        push_url = remote_url or clean_url

    try:
        subprocess.run(["git", "remote", "add", "origin", push_url], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print(f"  Could not add remote. Run: git remote add origin {clean_url} && git push -u origin main")
        return

    result = _run("git", "push", "-u", "origin", "main")
    if result.returncode == 0:
        reset_url = clean_url_override if clean_url_override is not None else clean_url
        if push_url != reset_url:
            _run("git", "remote", "set-url", "origin", reset_url)
        print(f"  Pushed to {clean_url.removesuffix('.git')}")
    else:
        print(f"  Could not push: {result.stderr.strip()}")
        print(f"  Run: git remote add origin {clean_url} && git push -u origin main")


def setup_develop_branch(repo_created, auth_url=None):
    """Create and push a develop branch, then set it as the default."""
    try:
        subprocess.run(["git", "checkout", "-b", "develop"], capture_output=True, check=True)
        print("  Created develop branch")
    except subprocess.CalledProcessError:
        print("  Could not create develop branch.")
        return

    if not repo_created:
        return

    if auth_url:
        _run("git", "remote", "set-url", "origin", auth_url)

    result = _run("git", "push", "-u", "origin", "develop")

    if auth_url:
        _run("git", "remote", "set-url", "origin", f"https://codeberg.org/{OWNER}/{REPO}.git")

    if result.returncode != 0:
        print(f"  Could not push develop branch: {result.stderr.strip()}")
        return
    print("  Pushed develop branch to origin")

    if GIT_HOSTING == "github":
        result = _run("gh", "api", "-X", "PATCH", f"repos/{OWNER}/{REPO}", "-f", "default_branch=develop")
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


# ---------------------------------------------------------------------------
# Instructions
# ---------------------------------------------------------------------------


def print_codeberg_instructions():
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


def print_pypi_trusted_publisher_instructions():
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


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    stamp_year()
    select_license("{{ cookiecutter.license }}")

    if DOCS_TYPE == "simple":
        shutil.rmtree("docs", ignore_errors=True)
        os.makedirs("docs")
        with open("docs/index.md", "w") as f:
            f.write(f"# {REPO}\n\nAdd your documentation here.\n")

    if GIT_HOSTING == "codeberg":
        shutil.rmtree(".github", ignore_errors=True)

        codeberg_user = preflight_codeberg()
        repo_created = bool(codeberg_user) and create_codeberg_repo(codeberg_user)

        token = os.environ.get("CODEBERG_TOKEN", "")
        auth_url = f"https://oauth2:{token}@codeberg.org/{OWNER}/{REPO}.git" if repo_created else None
        skip_reset = GIT_FLOW == "main_develop"

        generate_uv_lock()
        git_init_and_push(repo_created, remote_url=auth_url, clean_url_override=auth_url if skip_reset else None)

        if GIT_FLOW == "main_develop":
            setup_develop_branch(repo_created, auth_url=auth_url)

        if not repo_created:
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

        repo_created = False
        if preflight_github():
            repo_created = create_github_repo()
            if repo_created:
                enable_github_pages()
                if PUBLISH_TO_PYPI == "yes":
                    create_pypi_environment()

        generate_uv_lock()
        git_init_and_push(repo_created)

        if GIT_FLOW == "main_develop":
            setup_develop_branch(repo_created)

        if repo_created and GIT_FLOW in ("github_flow", "main_develop"):
            configure_branch_protection("main")
            if GIT_FLOW == "main_develop":
                configure_branch_protection("develop")

        if PUBLISH_TO_PYPI == "yes":
            print_pypi_trusted_publisher_instructions()

    print("Your Python package project has been created successfully!")
