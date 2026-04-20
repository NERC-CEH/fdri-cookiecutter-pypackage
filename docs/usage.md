# Usage

## Prerequisites

### uv

This template uses [uv](https://docs.astral.sh/uv/) for dependency management, and uv can also install and manage
Python for you.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

The installer should print a line telling you to restart your shell or `source` a file so `uv` ends up on your `PATH`.
Follow it, then verify:

```bash
uv --version
```

### Python 3.12+

Check whether you already have a suitable Python:

```bash
python3 --version
```

If you see `3.12.x` or newer, you're set. Otherwise, let uv fetch Python for you - this installs into uv's own
directory and doesn't touch any system Python:

```bash
uv python install 3.12
```

(You can skip this step if you prefer - `uv sync` later on will auto-install a matching Python when it reads the
generated project's `pyproject.toml`. Running it now just makes the failure mode clearer if something is wrong.)

### make

`make` is used as the task runner and is usually pre-installed on Linux. Check with:

```bash
make --version
```

If it's missing on Debian/Ubuntu:

```bash
sudo apt install make
```

### git

Most Linux distros ship with git; check with:

```bash
git --version
```

If it's missing, install with (on Debian/Ubuntu):

```bash
sudo apt install git
```

Then set the name and email that will appear on every commit:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@ceh.ac.uk"
```

### Hosting account

- **GitHub:** see [GitHub setup](usage-github.md#prerequisites)
- **Codeberg:** see [Codeberg setup](usage-codeberg.md#prerequisites)
- **None (local only):** no account needed — a local git repo is created with no remote

## Generating a project

Run the template with `uvx` (no install needed beyond uv):

```bash
uvx cookiecutter gh:NERC-CEH/fdri-cookiecutter-pypackage
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

## After generation

```bash
cd <package_name>
uv sync              # install all dependencies
make install-hooks   # configure git to use .githooks/
make qa              # format, lint, type-check, test
```

If you chose `sphinx` docs, preview them locally:

```bash
make docs-serve  # serves at http://localhost:8000
```

## Writing docs

The generated `docs/source/` directory contains `.rst` files to get you started, but you can use Markdown (`.md`) or
reStructuredText (`.rst`) - or mix both. [MyST-Parser](https://myst-parser.readthedocs.io/) is installed and
configured so Sphinx handles both formats automatically.

**Markdown example** - create `docs/source/my-page.md`:

```markdown
# My page

Some content here.
```

**reStructuredText example** - create `docs/source/my-page.rst`:

```rst
My page
=======

Some content here.
```

Then add the page to the table of contents in `docs/source/index.rst`:

```rst
.. toctree::

    my-page
```

Either format works - Sphinx should resolve the filename regardless of extension.

## Next steps

- [GitHub setup and post-generation steps](usage-github.md)
- [Codeberg setup and post-generation steps](usage-codeberg.md)
- [Git flows and branch protection](git-flows.md)
- [Releasing](releasing.md)
- [Troubleshooting](troubleshooting.md)
