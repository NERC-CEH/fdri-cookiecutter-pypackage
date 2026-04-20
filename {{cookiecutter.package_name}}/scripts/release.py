"""Tag the current version and{% if cookiecutter.git_hosting == "github" %} create a GitHub release.

On `main`: creates a git tag and GitHub release.
On `develop`: opens a release PR from develop to main instead.
{% elif cookiecutter.git_hosting == "codeberg" %} push the tag.

On `main`: creates an annotated git tag and pushes it.
On `develop`: opens a Codeberg PR (if CODEBERG_TOKEN is set) or prints the URL to do it manually.
{% else %} create a local annotated tag.

No remote is configured. The tag is created locally only.
{% endif %}"""

{% if cookiecutter.git_hosting == "codeberg" %}import json
import os
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path{% elif cookiecutter.git_hosting == "github" %}import subprocess
import sys
import tomllib
from pathlib import Path{% else %}import subprocess
import tomllib
from pathlib import Path{% endif %}
{% if cookiecutter.git_hosting == "codeberg" %}
OWNER = "{{ cookiecutter.repo_owner }}"
REPO = "{{ cookiecutter.package_name }}"


def _codeberg_api(path, method="GET", payload=None):
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
{% endif %}

def _run(*cmd: str) -> None:
    print(f"$ {' '.join(cmd)}")  # noqa: T201
    subprocess.run(cmd, check=True)


def _current_branch() -> str:
    return subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def main() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    version = pyproject["project"]["version"]
    tag = f"v{version}"{% if cookiecutter.git_hosting != "none" %}
    notes_path = Path(f"CHANGELOG/{version}.md")
    branch = _current_branch(){% endif %}{% if cookiecutter.git_hosting == "github" %}
    name = pyproject["project"]["name"]{% endif %}
{% if cookiecutter.git_hosting == "github" %}
    if branch == "develop":
        print(f"On develop - opening release PR for {tag} rather than tagging.")  # noqa: T201
        result = subprocess.run(
            [
                "gh",
                "pr",
                "create",
                "--base",
                "main",
                "--head",
                "develop",
                "--title",
                f"Release {tag}",
                "--body-file",
                str(notes_path),
            ],
            check=False,
        )
        if result.returncode != 0:
            print(  # noqa: T201
                "\nA release PR may already exist, or gh pr create failed.\n"
                "Check: gh pr list --base main\n"
                "After merging, run `make release` from main to tag and publish."
            )
        else:
            print(
                f"\nRelease PR opened for {tag}.\nAfter it is merged, run `make release` from main to tag and publish."
            )  # noqa: T201
        return

    if branch != "main":
        print(
            f"Error: `make release` must be run from main or develop, not '{branch}'.\n"
            f"Switch to the correct branch and try again."
        )  # noqa: T201
        sys.exit(1)

    lines = notes_path.read_text().splitlines(keepends=True)
    title = f"{name} {version}"
    if lines and lines[0].startswith("# "):
        title = lines[0].lstrip("# ").strip()
        lines = lines[1:]
        if lines and not lines[0].strip():
            lines = lines[1:]
    notes = "".join(lines).rstrip()

    _run("git", "tag", "-a", tag, "-m", f"Release {tag}")
    _run("git", "push", "origin", tag)
    _run("gh", "release", "create", tag, "--verify-tag", "--title", title, "--notes", notes)
{% elif cookiecutter.git_hosting == "codeberg" %}
    if branch == "develop":
        token = os.environ.get("CODEBERG_TOKEN")
        if token:
            print(f"On develop - opening release PR for {tag} on Codeberg.")  # noqa: T201
            notes = notes_path.read_text() if notes_path.exists() else ""
            status, body = _codeberg_api(
                f"/repos/{OWNER}/{REPO}/pulls",
                method="POST",
                payload={"title": f"Release {tag}", "body": notes, "head": "develop", "base": "main"},
            )
            if status in (200, 201):
                pr_url = body.get("html_url", f"https://codeberg.org/{OWNER}/{REPO}/pulls")
                print(f"\nRelease PR opened: {pr_url}")  # noqa: T201
                print("After it is merged, run `make release` from main to tag.")  # noqa: T201
            else:
                msg = body.get("message", str(body))
                print(f"Could not open PR (HTTP {status}): {msg}")  # noqa: T201
                print(f"Open manually: https://codeberg.org/{OWNER}/{REPO}/compare/main...develop")  # noqa: T201
        else:
            print(f"On develop - merge to main before tagging {tag}.")  # noqa: T201
            print(f"Open a PR: https://codeberg.org/{OWNER}/{REPO}/compare/main...develop")  # noqa: T201
            print("After it is merged, run `make release` from main.")  # noqa: T201
        return

    if branch != "main":
        print(
            f"Error: `make release` must be run from main or develop, not '{branch}'."
            f"\nSwitch to the correct branch and try again."
        )  # noqa: T201
        sys.exit(1)

    _run("git", "tag", "-a", tag, "-m", f"Release {tag}")
    _run("git", "push", "origin", tag)
    print(f"\nTag {tag} pushed.")  # noqa: T201
    print(f"Create the release at: https://codeberg.org/{OWNER}/{REPO}/releases/new?tag={tag}")  # noqa: T201
{% else %}
    _run("git", "tag", "-a", tag, "-m", f"Release {tag}")
    print(f"\nTag {tag} created locally.")  # noqa: T201
    print("When you add a remote, push it with: git push origin " + tag)  # noqa: T201
{% endif %}

if __name__ == "__main__":
    main()
