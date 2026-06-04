# FDRI Cookiecutter Templates

A set of [Cookiecutter](https://cookiecutter.readthedocs.io/) templates for new Python projects at UKCEH/FDRI.
Two templates live in this repo; select one with the `--directory` flag.

| Template                   | Use when                                                                                 |
|----------------------------|------------------------------------------------------------------------------------------|
| [`pypackage/`](pypackage/) | Building a Python library - something other projects import, or a tool published to PyPI |
| [`pyservice/`](pyservice/) | Building a Python service deployed to FDRI AWS - runs as a container                     |

## Quick start

Python package:

```bash
uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-templates --directory=pypackage
```

Python service:

```bash
uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-templates --directory=pyservice
```

## Documentation

Full documentation: https://nerc-ceh.github.io/fdri-cookiecutter-templates/

## Repo notes

- Shared files identical across templates live in [`_shared/`](_shared/) and are symlinked into each template.

## Releasing a new version

This repo uses a `main/develop/feature` gitflow. Features accumulate on `develop`; when a release is ready we
then merge `develop -> main`.

1. **On `develop`** - once you have all the features merged to develop you want to release, bump the version and
   write the changelog:

   ```bash
   make bump-patch   # 1.0.0 -> 1.0.1
   make bump-minor   # 1.0.0 -> 1.1.0
   make bump-major   # 1.0.0 -> 2.0.0
   ```

   This updates `pyproject.toml`, runs `uv lock`, commits both, and creates a `CHANGELOG/<version>.md` stub. Fill in the
   changelog and commit.

2. **Open a release PR** - run `make release` from `develop`. This opens a `develop -> main` PR automatically using the
   changelog as the PR body.

3. **The `release-ready` job** verifies the changelog is filled in before the PR can be merged to `main`.

4. **After merge to `main`** - run `make release` from `main`. This tags the commit and creates a GitHub release using
   the changelog as release notes.
