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
uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-pypackage --directory=pypackage
```

Python service:

```bash
uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-pypackage --directory=pyservice
```

## Documentation

Full documentation is in [`docs/`](docs/index.md). Key pages:

**pypackage** - [usage](docs/pypackage/usage.md) · [GitHub setup](docs/pypackage/usage-github.md) · [git flows](docs/pypackage/git-flows.md) · [releasing](docs/pypackage/releasing.md) · [troubleshooting](docs/pypackage/troubleshooting.md)

**pyservice** - [usage](docs/pyservice/usage.md) · [GitHub and AWS setup](docs/pyservice/usage-github.md) · [git flow](docs/pyservice/git-flows.md) · [releasing](docs/pyservice/releasing.md)

## Repo notes

- Repo currently named `fdri-cookiecutter-pypackage` for historical reasons; a rename to `fdri-cookiecutter` is planned.
- Shared files identical across templates live in [`_shared/`](_shared/) and are symlinked into each template.
