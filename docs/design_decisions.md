# Design decisions

Key choices made in this template and why.

## uv for dependency management

[uv](https://docs.astral.sh/uv/) replaces pip, pip-tools, and virtualenv in one tool. It is fast, lock-file based, and handles dependency
groups cleanly. The template uses dependency groups (`dev`, `test`, `lint`, `typecheck`, `docs`) so `uv sync`
installs exactly what each context needs.

`uv version --bump patch/minor/major` is also used for version bumping, so no extra tool is needed - see [Releasing](pypackage/releasing.md).

## Hatchling as the build backend

[Hatchling](https://hatch.pypa.io/latest/config/build/) is the default build backend for new packages in the
Python ecosystem (recommended by PyPA). It reads metadata from `pyproject.toml` directly and has no legacy baggage
from setuptools.

## `src` layout

The package lives under `src/<import_name>/` rather than at the repo root. This prevents accidentally importing
local source during tests (you always test the installed package) and is the recommended layout for new Python projects.

## `make` over `just`

`make` is probably already present on every developer machine and is more widely used (including for Sphinx).
Adding `just` would be an extra dependency for the same job.

## pyright for type checking

[pyright](https://microsoft.github.io/pyright/) is a static type checker for Python. It analyses your code without
running it, catching type errors, missing attributes, and incorrect function signatures at development time
rather than at runtime. It runs in basic mode so it flags real issues without requiring full type annotations
on every function.

## pytest with 90% coverage floor

`pytest` is the most common unit testing framework now, with useful features out of the box.
Unit test coverage is enforced at 90% via `[tool.coverage.report] fail_under = 90` in `pyproject.toml` which can be
altered if necessary.

## ruff for formatting and linting

[ruff](https://docs.astral.sh/ruff/) handles both code formatting and linting in a single tool. It enforces a consistent style across the
codebase and catches common errors. The pre-commit git hook runs `ruff format --check` and `ruff check` on every commit
so issues are caught locally before they reach CI.

## Reusable CI workflows from dri-cicd

CI uses `NERC-CEH/dri-cicd` reusable workflows rather than duplicating workflow YAML in every repo. The pipeline covers
testing, docs build, docs deploy. An additional local workflow handles the (optional) PyPI publishing.

## Sphinx

[Sphinx](https://www.sphinx-doc.org/) is an established Python documentation tool with a lot of documentation and help online. `sphinx-autodoc`
+ `autosummary` generate API reference pages from docstrings without requiring a separate tool.

[MyST-Parser](https://myst-parser.readthedocs.io/) is included so documentation pages can be written in either Markdown (`.md`) or reStructuredText
(`.rst`) - see [Writing docs](pypackage/usage.md#writing-docs) in the usage guide.

### Shibuya theme
Using a theme allows us to have consistency across FDRI packages.
The [Shibuya](https://shibuya.lepture.com/) theme gives a modern look and nice features to make documentation interesting to view.

## Optional docs

Not every project needs full Sphinx documentation. The `docs_type` prompt lets you choose:

- `sphinx` - full Sphinx setup; deploys to GitHub Pages on the GitHub path, local build only otherwise
- `simple` - a bare `docs/` directory for Markdown files, no build step

## Optional PyPI publishing

Internal tools often do not need to be on PyPI. The `publish_to_pypi` prompt controls whether `publish.yml`
is included. When enabled, [trusted publishing](https://docs.pypi.org/trusted-publishers/) is used so no API tokens are needed.

## Git flow options

The template offers three branching strategies rather than one to match the ceremony level to the project's scope.

- `simple` (single `main` branch) is the right default for most generated projects - one-off scripts, exploratory
analysis tools, and small internal utilities do not benefit from PR reviews and branch protection. Adding that
overhead by default would discourage use of the template.

- `github_flow` adds feature branches and PR-based protection on `main`. It suits small-team internal projects where
changes should be reviewed but there is no need to distinguish "released" from "in-progress" state on `main`.

- `main_develop` adds a `develop` integration branch so that `main` stays exactly in sync with what is published.
This matters most for PyPI packages, where the GitHub repo's default view (`main`) is what users see when they browse
the source - they expect it to match what they installed. Feature PRs target `develop`; releases go through a
`develop -> main` PR, and only after that merge is `main` tagged.

**Why `release.py` detects flow from branch name rather than a config file:** the current git branch is always up to
date and requires no extra bookkeeping. An option in a config file could become stale (e.g. if someone switches flow
conventions later). Checking the branch also makes the script's behaviour transparent - running `make release`
on `develop` does a PR; running it on `main` does a tag; running it anywhere else errors clearly.

## Hosting options (`git_hosting`)

Three hosting paths are supported:

- `github` - full automation: repo creation via `gh`, CI via `NERC-CEH/dri-cicd`, Pages deploy, branch protection,
and (optionally) trusted publishing to PyPI.
- `codeberg` - repo creation via the Forgejo REST API (when `CODEBERG_TOKEN` is set), but no CI, no hosted docs, and
no PyPI publishing. Codeberg has no official CLI and a different CI engine (Forgejo Actions); rather than shipping
a second set of reusable workflows, the Codeberg path deliberately omits them. The local scaffold is the same -
same tests, same Makefile, same linting.
- `none` - local git repo only, no remote. Useful for scratch projects or work that will be pushed somewhere else
later.

`make release` works on all three paths. On GitHub it tags, pushes, and creates a GitHub Release; on Codeberg it
tags, pushes, and prints the URL to create a release in the web UI; on `none` it creates a local tag only.

`publish_to_pypi=yes` is only valid with `git_hosting=github` - trusted publishing relies on GitHub's OIDC identity,
which has no equivalent on Codeberg or for a local-only repo. The combination is blocked in `pre_gen_project.py`.

## Two templates in one repo (`pypackage` and `pyservice`)

A Python library and a Python service have different deployment targets, different CI pipelines, and different
release conventions - but the same development tooling (uv, ruff, pytest, pyright, Sphinx) and the same project
scaffold (src layout, Makefile, CHANGELOG, CITATION.cff, etc.).

Keeping both templates in one repo means:

- a single place to update shared tooling decisions (e.g. upgrading to a new Python version or ruff release)
- shared docs and conventions live in one place

The alternative would be separate repos - which would be more difficult to synchronise changes across both.

Cookiecutter's `--directory` flag (e.g. `--directory=pypackage`) selects which subdirectory to treat as the
template root. Everything outside that directory is invisible to the user.
See: https://cookiecutter.readthedocs.io/en/1.7.2/advanced/directories.html

## Symlinks for shared template files (`_shared/`)

Many files are identical across `pypackage` and `pyservice` - e.g. the `src/` skeleton, `tests/`, Sphinx config,
CHANGELOG stub, `pyproject.toml`, `.githooks/`, etc.

Files that are identical live in `_shared/{{cookiecutter.package_name}}/` and are symlinked into both
template directories. Cookiecutter follows symlinks when copying files, so generated projects receive
real file copies - symlinks are a detail of the template repo structure, invisible to users.

A script (`make sync-symlinks`) regenerates all symlinks from `_shared/` in case they are accidentally removed or
a new shared file is added. A test suite (`tests/test_shared_symlinks.py`) asserts that every file in `_shared/`
has a corresponding valid symlink in both templates, and runs as part of CI to try and guard against files being missed.

## Shared hook code (`_shared/hooks/hook_utils.py`)

Both templates have a `post_gen_project.py` hook that does similar work - preflighting `gh`, creating the GitHub
repo, enabling Pages, configuring branch protection, generating `uv.lock`. Rather than duplicate the helpers in
each hook, the shared ones live in `_shared/hooks/hook_utils.py` and are imported from both hooks at render time:

```python
_TEMPLATE_DIR = "{{ cookiecutter._template }}"
sys.path.insert(0, os.path.normpath(os.path.join(_TEMPLATE_DIR, "..", "_shared", "hooks")))
from hook_utils import preflight_github, create_github_repo, ...
```

Cookiecutter sets `cookiecutter._template` to the template directory path, so `../_shared/hooks/` resolves to the
repo root's `_shared/hooks/` regardless of where the template was cloned to (local checkout, `~/.cookiecutters/`
cache, or a CI runner's temp dir). Template-specific logic (commit message, Codeberg API, AWS secrets prompt,
3-branch git init) stays in each hook; the shared functions are parameterised where the two templates diverge
(`default_visibility`, `warn_branch_protection`).

Bake tests pass the template as a relative path, which cookiecutter preserves as-is in `_template`. Tests resolve
to an absolute path so the hook can find `_shared/hooks/` after cookiecutter changes cwd to the generated project
directory. Real users always hit this via an absolute path (either a local absolute path or a cloned cache dir).

A function-based approach was chosen over a class hierarchy: the two templates only diverge on two parameters, so
class inheritance would be ceremony without payoff. If a third template lands or divergence grows, revisit.

## CHANGELOG directory

Releases are tracked in `CHANGELOG/<version>.md` files rather than a single append-only file. Each release gets its
own file, making it easy to see what changed in a given version and reducing merge conflicts.
