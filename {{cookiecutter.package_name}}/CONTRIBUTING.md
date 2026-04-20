# Contributing

Contributions are welcome and greatly appreciated.

## Types of Contributions

### Report Bugs

{% if cookiecutter.git_hosting != "none" %}Report bugs at https://{% if cookiecutter.git_hosting == "github" %}github.com{% else %}codeberg.org{% endif %}/{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}/issues.{% else %}Report bugs directly to the project maintainer.{% endif %}

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

{% if cookiecutter.git_hosting != "none" %}
### Fix Bugs

Look through the {% if cookiecutter.git_hosting == "github" %}GitHub{% else %}Codeberg{% endif %} issues for bugs - these are open to whoever wants to implement it.

### Implement Features

Look through the {% if cookiecutter.git_hosting == "github" %}GitHub{% else %}Codeberg{% endif %} issues for features - these are open to whoever wants to implement it.

### Write Documentation

{{ cookiecutter.project_name }} could always use more documentation, whether as part of the official docs, local
README's or in docstrings, and comments.

To preview the official docs locally:

```sh
make docs-serve
```

This starts a local server at http://localhost:8000 with live reload. Edit files in `docs/` or add docstrings
to your code (the API reference page is auto-generated).

{% endif %}
### Submit Feedback

{% if cookiecutter.git_hosting != "none" %}The best way to send feedback is to file an issue at
https://{% if cookiecutter.git_hosting == "github" %}github.com{% else %}codeberg.org{% endif %}/{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}/issues.{% else %}The best way to send feedback is to contact the project maintainer directly.{% endif %}

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.

{% if cookiecutter.git_hosting != "none" %}
## Get Started

Ready to contribute? Here's how to set up {{ cookiecutter.package_name }} for local development.

1. Fork the {{ cookiecutter.package_name }} repo on {% if cookiecutter.git_hosting == "github" %}GitHub{% else %}Codeberg{% endif %}.

1. Clone your fork locally:

   ```sh
   git clone git@{% if cookiecutter.git_hosting == "github" %}github.com{% else %}codeberg.org{% endif %}:your_name_here/{{ cookiecutter.package_name }}.git
   ```

1. Install your local copy with uv:

   ```sh
   cd {{ cookiecutter.package_name }}/
   uv sync
   ```
{% if cookiecutter.git_flow == "simple" %}

1. Create a branch for local development:

   ```sh
   git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

1. When you're done making changes, check that your changes pass linting and the tests:

   ```sh
   make qa
   ```

1. Commit your changes{% if cookiecutter.git_hosting != "none" %} and push your branch to {% if cookiecutter.git_hosting == "github" %}GitHub{% else %}Codeberg{% endif %}{% endif %}:

   ```sh
   git add .
   git commit -m "Your detailed description of your changes."
{% if cookiecutter.git_hosting != "none" %}   git push origin name-of-your-bugfix-or-feature
{% endif %}   ```

1. {% if cookiecutter.git_hosting != "none" %}Submit a pull request through the {% if cookiecutter.git_hosting == "github" %}GitHub{% else %}Codeberg{% endif %} website.{% else %}Merge your branch into main locally when ready.{% endif %}
{% elif cookiecutter.git_flow == "github_flow" %}

1. Create a branch for local development off `main`:

   ```sh
   git checkout main
   git pull origin main
   git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

1. When you're done making changes, check that your changes pass linting and the tests:

   ```sh
   make qa
   ```

1. Commit your changes{% if cookiecutter.git_hosting != "none" %} and push your branch to {% if cookiecutter.git_hosting == "github" %}GitHub{% else %}Codeberg{% endif %}{% endif %}:

   ```sh
   git add .
   git commit -m "Your detailed description of your changes."
{% if cookiecutter.git_hosting != "none" %}   git push origin name-of-your-bugfix-or-feature
{% endif %}   ```

1. {% if cookiecutter.git_hosting != "none" %}Open a pull request targeting `main` through the {% if cookiecutter.git_hosting == "github" %}GitHub{% else %}Codeberg{% endif %} website.{% else %}Merge your branch into main locally when ready.{% endif %}
{% if cookiecutter.git_hosting == "github" %}
   **Branch protection on `main`:**
   - At least 1 approving review is required before merge.
   - CI checks (`test-python`{% if cookiecutter.docs_type == "sphinx" %}, `build-docs`{% endif %}) must pass.
   - All PR review conversations must be resolved.
{%- endif %}
{% elif cookiecutter.git_flow == "main_develop" %}

1. Create a branch for local development off `develop`:

   ```sh
   git checkout develop
   git pull origin develop
   git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

1. When you're done making changes, check that your changes pass linting and the tests:

   ```sh
   make qa
   ```

1. Commit your changes{% if cookiecutter.git_hosting != "none" %} and push your branch to {% if cookiecutter.git_hosting == "github" %}GitHub{% else %}Codeberg{% endif %}{% endif %}:

   ```sh
   git add .
   git commit -m "Your detailed description of your changes."
{% if cookiecutter.git_hosting != "none" %}   git push origin name-of-your-bugfix-or-feature
{% endif %}   ```

1. {% if cookiecutter.git_hosting != "none" %}Open a pull request targeting `develop` through the {% if cookiecutter.git_hosting == "github" %}GitHub{% else %}Codeberg{% endif %} website.{% else %}Merge your branch into develop locally when ready.{% endif %}
{% if cookiecutter.git_hosting == "github" %}
   **Branch protection on `develop` and `main`:**
   - At least 1 approving review is required before merge.
   - CI checks (`test-python`{% if cookiecutter.docs_type == "sphinx" %}, `build-docs`{% endif %}) must pass.
   - All PR review conversations must be resolved.
{%- endif %}
{%- endif %}

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function
with a docstring, and add the feature to the list in README.md.
3. The pull request should pass all quality checks (`make qa`){% if cookiecutter.git_hosting == "github" %} and GitHub Actions{% elif cookiecutter.git_hosting == "codeberg" %} (no CI is configured by default){% endif %}, making sure that the tests pass for all supported Python versions.

## Tips

To run a subset of tests:

```sh
uv run pytest tests/
```

## Releasing a New Version
{% if cookiecutter.git_flow == "simple" %}
1. **Bump the version** and create a CHANGELOG stub:
   ```bash
   make bump-patch   # or bump-minor / bump-major
   ```
   This updates `pyproject.toml`, commits the bump, and creates `CHANGELOG/<version>.md`.

2. **Fill in** `CHANGELOG/<version>.md` with the release notes, then commit{% if cookiecutter.git_hosting != "none" %} and push{% endif %}:
   ```bash
   git add CHANGELOG/<version>.md
   git commit -m "Add release notes for <version>"
{% if cookiecutter.git_hosting != "none" %}   git push origin main
{% endif %}   ```

3. **Release:**
   ```bash
   make release
   ```
{% if cookiecutter.git_hosting == "github" %}   This creates an annotated `v*` tag, pushes it to GitHub, and creates a
   GitHub Release with the changelog contents as release notes.
{% elif cookiecutter.git_hosting == "codeberg" %}   This creates an annotated tag and pushes it. You'll be shown the URL to create a release on Codeberg.
{% else %}   This creates a local annotated tag. Push it when you have a remote configured.
{% endif %}
{% elif cookiecutter.git_flow == "github_flow" %}

1. **On `main`**, bump the version and create a CHANGELOG stub:
   ```bash
   make bump-patch   # or bump-minor / bump-major
   ```
   This updates `pyproject.toml`, commits the bump, and creates `CHANGELOG/<version>.md`.

2. **Fill in** `CHANGELOG/<version>.md` with the release notes, then commit{% if cookiecutter.git_hosting != "none" %} and push{% endif %}:
   ```bash
   git add CHANGELOG/<version>.md
   git commit -m "Add release notes for <version>"
{% if cookiecutter.git_hosting != "none" %}   git push origin main
{% endif %}   ```

3. **Release:**
   ```bash
   make release
   ```
{% if cookiecutter.git_hosting == "github" %}   This creates an annotated `v*` tag, pushes it to GitHub, and creates a
   GitHub Release with the changelog contents as release notes.
{% elif cookiecutter.git_hosting == "codeberg" %}   This creates an annotated tag and pushes it. You'll be shown the URL to create a release on Codeberg.
{% else %}   This creates a local annotated tag. Push it when you have a remote configured.
{% endif %}
{% elif cookiecutter.git_flow == "main_develop" %}

Releases go through `develop` -> `main` to keep `main` in sync with what is published.

1. **On `develop`**, bump the version and create a CHANGELOG stub:
   ```bash
   git checkout develop
   git pull origin develop
   make bump-patch   # or bump-minor / bump-major
   ```
   This updates `pyproject.toml`, commits the bump, and creates `CHANGELOG/<version>.md`.

2. **Fill in** `CHANGELOG/<version>.md` with the release notes, then commit{% if cookiecutter.git_hosting != "none" %} and push{% endif %}:
   ```bash
   git add CHANGELOG/<version>.md
   git commit -m "Add release notes for <version>"
{% if cookiecutter.git_hosting != "none" %}   git push origin develop
{% endif %}   ```

{% if cookiecutter.git_hosting == "github" %}
3. **Open a release PR** from develop to main:
   ```bash
   make release
   ```
   When run from `develop`, this opens a pull request against `main` using the CHANGELOG
   as the PR description.

4. **After the PR is merged**, switch to `main` and tag:
   ```bash
   git checkout main
   git pull origin main
   make release
   ```
   When run from `main`, this creates an annotated `v*` tag, pushes it to GitHub, and
   creates a GitHub Release.
{% elif cookiecutter.git_hosting == "codeberg" %}
3. **Open a release PR** from develop to main:
   ```bash
   make release
   ```
   This opens a Codeberg PR (if `CODEBERG_TOKEN` is set) or prints the URL to open one manually.

4. **After the PR is merged**, switch to `main` and tag:
   ```bash
   git checkout main
   git pull origin main
   make release
   ```
   This creates an annotated tag, pushes it, and shows the URL to create a release on Codeberg.
{% else %}
3. **Merge develop into main** locally:
   ```bash
   git checkout main
   git merge develop
   ```

4. **Tag the release:**
   ```bash
   make release
   ```
   This creates a local annotated tag. Push the tag when you have a remote configured.
{% endif %}
{% endif %}
{% endif %}
