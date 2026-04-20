# FDRI Python Package Template

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template for new Python packages at UKCEH/FDRI. It generates a
ready-to-go project with CI/CD, optional Sphinx docs, and optional PyPI publishing already wired up.

## Quick start

```bash
uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-pypackage
```

Answer the prompts and your project is created - git-initialised and ready to push. Supports remote hosting on GitHub
and Codeberg, as well as a simple local-only setup for projects with no remote host configured.

## What gets generated

- **Source layout** - `src/<package>/` with `__init__.py` and `__main__.py`
- **Tests** - `pytest` with coverage enforced at 90%
- **Makefile** - `make qa`, `make test`, `make docs-serve`, and more
- **Git hooks** - `ruff` format and lint check on every commit (via `.githooks/`)
- **Optional Sphinx docs** - Shibuya theme, autodoc
- **Optional PyPI publishing** - trusted publishing to PyPI (GitHub only)

### Git hosting (`git_hosting`)

Choose where your project lives:

| Feature                    | `github` (default)                                 | `codeberg`                   | `none`                          |
|----------------------------|----------------------------------------------------|------------------------------|---------------------------------|
| Repo created automatically | Yes (via `gh` CLI)                                 | Yes (if CODEBERG_TOKEN set)  | No                              |
| CI workflows               | GitHub Actions (reusable from `NERC-CEH/dri-cicd`) | None                         | None                            |
| Hosted docs                | GitHub Pages                                       | Local build only             | Local build only                |
| PyPI publishing            | Trusted publishing via GitHub Actions              | Not available                | Not available                   |
| Branch protection          | Configured via `gh api`                            | Manual via Codeberg web UI   | N/A                             |
| Release script             | `make release` (tags + GitHub Release)             | `make release` (tags + push) | `make release` (local tag only) |

## Documentation

See [`docs/`](docs/index.md) for full usage guidance and design decisions.
