"""Bump the project version, commit, and create a CHANGELOG stub."""

import subprocess
import sys
import tomllib
from pathlib import Path

PYPROJECT = Path("pyproject.toml")


def _read_version() -> str:
    """Read the current project version from pyproject.toml.

    Returns:
        Version string.
    """
    return tomllib.loads(PYPROJECT.read_text())["project"]["version"]


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("major", "minor", "patch"):
        print("Usage: bump.py [major|minor|patch]")
        sys.exit(1)

    part = sys.argv[1]
    old_version = _read_version()

    subprocess.run(["uv", "version", "--bump", part], check=True)
    new_version = _read_version()

    subprocess.run(["git", "add", str(PYPROJECT)], check=True)
    subprocess.run(["git", "commit", "-m", f"Bump version: {old_version} -> {new_version}"], check=True)

    changelog_path = Path(f"CHANGELOG/{new_version}.md")
    if not changelog_path.exists():
        changelog_path.write_text(f"# {new_version}\n\n<!-- Add release notes here -->\n")
        subprocess.run(["git", "add", str(changelog_path)], check=True)
        subprocess.run(["git", "commit", "-m", f"Add CHANGELOG/{new_version}.md stub"], check=True)

    print()
    print(f"  Bumped to {new_version}.")
    print(f"  Fill in CHANGELOG/{new_version}.md with your release notes, then commit and push.")
    print()


if __name__ == "__main__":
    main()
