# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

* [GitHub](https://github.com/{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}/){% if cookiecutter.docs_type == "sphinx" %} | [Documentation](https://{{ cookiecutter.repo_owner }}.github.io/{{ cookiecutter.package_name }}/){% endif %}

## Deployment

This service uses a `staging` / `production` branching model. Each branch maps to a separate AWS account.

* Feature branches -> PR into `staging` (staging AWS account)
* `staging` -> auto-PR opened into `production` (production AWS account)

See [`docs/deployment.md`](./docs/deployment.md) for the full flow and the required GitHub repo secrets.

## Features

* TODO
{% if cookiecutter.docs_type == "sphinx" %}
## Documentation

Documentation is built with [Sphinx](https://www.sphinx-doc.org/) and deployed to GitHub Pages.

* **Live site:** https://{{ cookiecutter.repo_owner }}.github.io/{{ cookiecutter.package_name }}/
* **Preview locally:** `make docs-serve` (serves at http://localhost:8000)
* **Build:** `make docs-build`
{% endif %}
## Development

To set up for local development:

```bash
git clone git@github.com:{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}.git
cd {{ cookiecutter.package_name }}
uv sync
```

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
make qa
```

Build and run the Docker image locally:

```bash
make docker-build
make docker-run
```

## Citation

If you use this software, please cite it using the metadata in [`CITATION.cff`](./CITATION.cff).

## Licence

{{ cookiecutter.license }}

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [NERC-CEH/fdri-cookiecutter-pypackage](https://github.com/NERC-CEH/fdri-cookiecutter-pypackage) template (`pyservice`).
