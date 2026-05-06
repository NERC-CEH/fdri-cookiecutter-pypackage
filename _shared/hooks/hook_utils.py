"""Shared helpers for fdri-cookiecutter post-generation hooks.

Imported by both `pypackage/hooks/post_gen_project.py` and `pyservice/hooks/post_gen_project.py` via
`{{cookiecutter._template}}/../_shared/hooks` on sys.path at render time.
"""

import json
import os
import pathlib
import shutil
import subprocess
from datetime import datetime
from typing import Any


def stamp_year() -> None:
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


def select_license(license_choice: str) -> None:
    """Rename the chosen license file to LICENSE and remove the unused alternatives.

    Args:
        license_choice: The license value from cookiecutter, e.g. ``"MIT"`` or ``"GNU GPL v3.0"``.
    """
    license_files = {"MIT": "LICENSE.MIT", "GNU GPL v3.0": "LICENSE.GPL"}
    for name, filename in license_files.items():
        p = pathlib.Path(filename)
        if not p.exists():
            continue
        if name == license_choice:
            p.rename("LICENSE")
        else:
            p.unlink()


def run(*args: str, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    """Thin wrapper around subprocess.run that captures output and text by default."""
    kwargs.setdefault("capture_output", True)
    kwargs.setdefault("text", True)
    kwargs.setdefault("check", False)
    return subprocess.run(args, **kwargs)


def preflight_github(owner: str, repo: str, warn_branch_protection: bool = False) -> bool:
    """Verify gh CLI authentication and token scopes before any GitHub API calls.

    Args:
        owner: GitHub org or username that will own the repo.
        repo: Repository name.
        warn_branch_protection: Emit a note about GitHub Pro when the authenticated user owns the repo directly

    Returns:
        True if setup can proceed, False to skip all GitHub steps.
    """
    if not shutil.which("gh"):
        print("  gh CLI not found - skipping GitHub setup.")
        print(f"  Create manually: https://github.com/new?name={repo}&owner={owner}")
        return False

    if run("gh", "auth", "status").returncode != 0:
        print("  gh is not authenticated - skipping GitHub setup.")
        print("  Run 'gh auth login' then re-run cookiecutter.")
        return False

    result = run("gh", "api", "user", "--include")
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
        run("gh", "auth", "refresh", "-s", "workflow")

    current_user = run("gh", "api", "user", "-q", ".login").stdout.strip()

    if current_user and current_user.lower() != owner.lower():
        org_check = run("gh", "api", f"orgs/{owner}/memberships/{current_user}")
        if org_check.returncode != 0:
            print(f"  Logged in as '{current_user}' but no access to '{owner}' - skipping GitHub setup.")
            return False

    if warn_branch_protection and current_user and current_user.lower() == owner.lower():
        print("  Note: branch protection on private repos requires GitHub Pro for personal accounts.")

    return True


def create_github_repo(owner: str, repo: str, description: str, default_visibility: str = "public") -> bool:
    """Create the GitHub repo, prompting the user for public/private visibility.

    Args:
        owner: GitHub org or username.
        repo: Repository name.
        description: One-line repo description passed to the GitHub API.
        default_visibility: Visibility used when the user presses Enter without input.

    Returns:
        True if the repo was created or already existed, False on failure.
    """
    if not os.isatty(0):
        return False

    prompt = f"  Make the GitHub repo public or private? [public/private] ({default_visibility}): "
    choice = input(prompt).strip().lower()
    if choice not in ("public", "private"):
        choice = default_visibility
    visibility = f"--{choice}"

    result = run(
        "gh",
        "repo",
        "create",
        f"{owner}/{repo}",
        visibility,
        "--description",
        description,
    )
    if result.returncode == 0:
        print(f"  GitHub repo created: https://github.com/{owner}/{repo}")
        return True
    elif "already exists" in result.stderr:
        print(f"  GitHub repo {owner}/{repo} already exists")
        return True
    else:
        print(f"  Could not create repo: {result.stderr.strip()}")
        print(f"  Create manually: https://github.com/new?name={repo}&owner={owner}")
        return False


def enable_github_pages(owner: str, repo: str) -> None:
    """Enable GitHub Pages via the Actions source.

    Args:
        owner: GitHub org or username.
        repo: Repository name.
    """
    if not shutil.which("gh"):
        print("  gh CLI not found, skipping GitHub Pages setup.")
        print("  Enable manually: Settings > Pages > Source > GitHub Actions")
        return

    run("gh", "api", f"repos/{owner}/{repo}/pages", "-X", "POST", "-f", "build_type=workflow")
    run("gh", "api", f"repos/{owner}/{repo}/pages", "-X", "PUT", "-f", "build_type=workflow")
    print(f"  GitHub Pages enabled for {owner}/{repo} (source: GitHub Actions)")


def configure_branch_protection(owner: str, repo: str, branch: str, contexts: list[str]) -> None:
    """Apply branch protection rules via the GitHub REST API.

    Args:
        owner: GitHub org or username.
        repo: Repository name.
        branch: Branch to protect.
        contexts: Required status-check context names (e.g. ``["test-python"]``).
    """
    if not shutil.which("gh"):
        print(f"  gh CLI not found, skipping branch protection for {branch}.")
        print(f"  Enable manually: Settings > Branches > Add rule for '{branch}'")
        return

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
        ["gh", "api", "-X", "PUT", f"repos/{owner}/{repo}/branches/{branch}/protection", "--input", "-"],
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


def generate_uv_lock() -> None:
    """Generate uv.lock so CI's ``uv sync --locked`` has a pinned lockfile to validate against."""
    if not shutil.which("uv"):
        print("  uv not found - skipping uv.lock generation.")
        print("  Install uv and run 'uv lock' before pushing, or CI will fail.")
        return

    result = run("uv", "lock")
    if result.returncode == 0:
        print("  Generated uv.lock")
    else:
        print(f"  'uv lock' failed: {result.stderr.strip()}")
        print("  Run 'uv lock' manually before pushing, or CI will fail.")
