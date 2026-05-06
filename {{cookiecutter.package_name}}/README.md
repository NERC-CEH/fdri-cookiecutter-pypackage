# {{ cookiecutter.project_name }}

{% if cookiecutter.publish_to_pypi == "yes" %}![PyPI version](https://img.shields.io/pypi/v/{{ cookiecutter.package_name }}.svg)

{% endif %}{{ cookiecutter.project_short_description }}
{% if cookiecutter.git_hosting == "github" %}
* [GitHub](https://github.com/{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}/){% if cookiecutter.docs_type == "sphinx" %} | [Documentation](https://{{ cookiecutter.repo_owner }}.github.io/{{ cookiecutter.package_name }}/){% endif %}
{% elif cookiecutter.git_hosting == "codeberg" %}
* [Codeberg](https://codeberg.org/{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}/)
{% endif %}
## Features

* TODO
{% if cookiecutter.docs_type == "sphinx" %}
## Documentation

Documentation is built with [Sphinx](https://www.sphinx-doc.org/){% if cookiecutter.git_hosting == "github" %} and deployed to GitHub Pages{% endif %}.

{% if cookiecutter.git_hosting == "github" %}* **Live site:** https://{{ cookiecutter.repo_owner }}.github.io/{{ cookiecutter.package_name }}/
{% endif %}* **Preview locally:** `make docs-serve` (serves at http://localhost:8000)
* **Build:** `make docs-build`

API documentation is auto-generated from docstrings using [sphinx-autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html).
{% endif %}
## Development

To set up for local development:

```bash
{% if cookiecutter.git_hosting != "none" %}git clone git@{% if cookiecutter.git_hosting == "github" %}github.com{% else %}codeberg.org{% endif %}:{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}.git
{% endif %}cd {{ cookiecutter.package_name }}
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

## Citation

If you use this software, please cite it using the metadata in [`CITATION.cff`](./CITATION.cff).

## Licence

{{ cookiecutter.license }}

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [NERC-CEH/fdri-cookiecutter-pypackage](https://github.com/NERC-CEH/fdri-cookiecutter-pypackage) template.
