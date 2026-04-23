# pyservice usage

## Prerequisites

Install [uv, Python 3.12+, make, and git](../prerequisites.md) first.

### Docker

The generated service runs in a container. You will need Docker installed to build and test the image locally:

```bash
docker --version
```

See [Docker's install guide](https://docs.docker.com/engine/install/) if it's missing.

### GitHub account and gh CLI

See [GitHub and AWS setup](usage-github.md) for the full prerequisite list, including AWS OIDC roles.

## Generating a project

```bash
uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-pypackage --directory=pyservice
```

## Prompts

| Prompt                      | Default            | Notes                                                                         |
|-----------------------------|--------------------|-------------------------------------------------------------------------------|
| `project_name`              | `My Service`       | Human-readable name, e.g. `FDRI Ingest`                                       |
| `package_name`              | derived            | Repo/directory name, e.g. `fdri-ingest`                                       |
| `import_name`               | derived            | Python import name, e.g. `fdri_ingest`                                        |
| `project_short_description` | -                  | One-line description, used in `pyproject.toml` and the repo                   |
| `full_name`                 | -                  | Your name, goes in `pyproject.toml` authors                                   |
| `email`                     | `author@ceh.ac.uk` | Your email                                                                    |
| `organisation`              | `UKCEH`            | Your organisation name                                                        |
| `repo_username`             | -                  | Your GitHub username (used for authentication checks)                         |
| `first_version`             | `0.1.0`            | Starting version in `pyproject.toml`                                          |
| `license`                   | `GNU GPL v3.0`     | Recorded in `pyproject.toml`                                                  |
| `docs_type`                 | `sphinx`           | `sphinx` builds a full Sphinx site; `simple` creates a bare `docs/` directory |

Unlike `pypackage`, there are no prompts for `git_hosting`, `git_flow`, or `publish_to_pypi` - services always use
GitHub, the fixed `main -> staging -> production` flow, and are never published to PyPI. The repo owner is always
`NERC-CEH` and cannot be changed.

## After generation

**Before the first push to `main` will trigger a successful deploy**, you must add four AWS secrets to the GitHub
repository. See [GitHub and AWS setup](usage-github.md#aws-secrets) for the exact steps.

See [After generation](../after-generation.md) for citation metadata and writing docs.

## Next steps

- [Releasing](releasing.md)
