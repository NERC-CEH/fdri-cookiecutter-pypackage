"""Regenerate symlinks in pypackage and pyservice pointing into _shared/."""

import os
import pathlib
import sys


def sync(repo: pathlib.Path) -> None:
    """Recreate all symlinks from _shared/ into pypackage/ and pyservice/.

    For each file in ``_shared/{{cookiecutter.package_name}}/``, ensures a symlink exists at the corresponding
    path in both template directories. Existing symlinks are replaced.

    Args:
        repo: Root of the cookiecutter repository.
    """
    shared_root = repo / "_shared" / "{{cookiecutter.package_name}}"
    if not shared_root.exists():
        print(f"ERROR: {shared_root} not found", file=sys.stderr)
        sys.exit(1)

    for template in ["pypackage", "pyservice"]:
        tmpl_pkg = repo / template / "{{cookiecutter.package_name}}"
        for src in shared_root.rglob("*"):
            if not src.is_file():
                continue
            rel = src.relative_to(shared_root)
            dst = tmpl_pkg / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            target = os.path.relpath(src, dst.parent)
            if dst.is_symlink():
                dst.unlink()
            elif dst.exists():
                print(f"SKIP (real file, not a symlink): {dst}")
                continue
            dst.symlink_to(target)
            print(f"  {dst} -> {target}")


if __name__ == "__main__":
    REPO = pathlib.Path(__file__).parent.parent
    sync(REPO)
    print("Done.")
