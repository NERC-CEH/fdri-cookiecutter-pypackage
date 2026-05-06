# FDRI Cookiecutter Templates

Two templates live in this repo. Choose based on what you're building:

| Template                          | Use when                                                                                 | Quick start                                                                      |
|-----------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| [`pypackage`](pypackage/usage.md) | Building a Python library - something other projects import, or a tool published to PyPI | `uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-pypackage --directory=pypackage` |
| [`pyservice`](pyservice/usage.md) | Building a Python service deployed to FDRI AWS - runs as a container                     | `uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-pypackage --directory=pyservice` |

If you are unsure, ask!

## Shared guides

- [Prerequisites](prerequisites.md) - uv, Python 3.12+, make, and git (required by both templates)
- [After template generation](after-generation.md) - standard setup steps, citation metadata, writing docs

## pypackage docs

- [Usage](pypackage/usage.md) - prerequisites, prompts, post-generation steps
- [GitHub setup](pypackage/usage-github.md) - `gh` CLI, account auth, PyPI publishing
- [Codeberg setup](pypackage/usage-codeberg.md) - `CODEBERG_TOKEN`, account setup
- [Git flows and branch protection](pypackage/git-flows.md) - picking a branching strategy
- [Releasing](pypackage/releasing.md) - bumping versions, tagging, publishing to PyPI
- [Troubleshooting](pypackage/troubleshooting.md) - common issues and fixes

## pyservice docs

- [Usage](pyservice/usage.md) - prerequisites, prompts, post-generation steps
- [GitHub and AWS setup](pyservice/usage-github.md) - `gh` CLI, AWS OIDC secrets
- [Git flow](pyservice/git-flows.md) - `staging -> production` model
- [Releasing](pyservice/releasing.md) - bumping versions, deploying to production

## Repo notes

- [Design decisions](design_decisions.md) - why we made the choices we did
- Repo currently named `fdri-cookiecutter-pypackage` for historical reasons; a rename to `fdri-cookiecutter` is planned
