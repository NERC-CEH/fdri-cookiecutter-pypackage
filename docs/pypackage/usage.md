# Usage

## Prerequisites

Install [uv, Python 3.12+, make, and git](../prerequisites.md) first.

### Hosting account

- **GitHub:** see [GitHub setup](usage-github.md#prerequisites)
- **Codeberg:** see [Codeberg setup](usage-codeberg.md#prerequisites)
- **None (local only):** no account needed - a local git repo is created with no remote

## Generating a project

Run the template with `uvx` (no install needed beyond uv):

```bash
uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-pypackage --directory=pypackage
```

## Prompts

| Prompt                      | Default            | Notes                                                                                    |
|-----------------------------|--------------------|------------------------------------------------------------------------------------------|
| `project_name`              | `My Package`       | Human-readable name, e.g. `FDRI Rainfall`                                                |
| `package_name`              | derived            | Repo/directory name, e.g. `fdri-rainfall`                                                |
| `import_name`               | derived            | Python import name, e.g. `fdri_rainfall`                                                 |
| `project_short_description` | -                  | One-line description, used in `pyproject.toml` and the repo                              |
| `full_name`                 | -                  | Your name, goes in `pyproject.toml` authors                                              |
| `email`                     | `author@ceh.ac.uk` | Your email                                                                               |
| `organisation`              | `UKCEH`            | Your organisation name, recorded in `pyproject.toml`                                     |
| `git_hosting`               | `github`           | `github` for full CI/CD; `codeberg` for a simpler scaffold; `none` for a local-only repo |
| `repo_username`             | -                  | Your personal username on the chosen host (unused for `none`)                            |
| `repo_owner`                | `repo_username`    | Organisation or username that will own the repo (unused for `none`)                      |
| `first_version`             | `0.1.0`            | Starting version in `pyproject.toml`                                                     |
| `license`                   | `GNU GPL v3.0`     | Recorded in `pyproject.toml`                                                             |
| `publish_to_pypi`           | `no`               | `yes` adds `publish.yml` and PyPI setup instructions (GitHub only)                       |
| `git_flow`                  | `simple`           | Branching workflow - see [Choosing a git flow](git-flows.md)                             |
| `docs_type`                 | `sphinx`           | `sphinx` builds a full Sphinx site; `simple` creates a bare `docs/` directory            |

### Helpful links

- [GitHub setup and post-generation steps](usage-github.md)
- [Codeberg setup and post-generation steps](usage-codeberg.md)
- [Git flows and branch protection](git-flows.md)

## After generation

See [After generation](../after-generation.md) for the standard setup steps, citation metadata, and writing docs.

## Next steps

- [Releasing](releasing.md)
- [Troubleshooting](troubleshooting.md)
