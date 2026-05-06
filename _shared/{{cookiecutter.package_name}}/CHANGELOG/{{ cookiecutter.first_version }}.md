{% set git_hosting = cookiecutter._git_hosting if cookiecutter._git_hosting is defined else cookiecutter.git_hosting %}
## {{ cookiecutter.project_name }} {{ cookiecutter.first_version }}

{{ cookiecutter.project_short_description }}

This release establishes the project scaffold.

### What's in the scaffold

- `src/{{ cookiecutter.import_name }}/` package with `__init__` and `__main__`
- Tests with pytest and coverage (90% threshold)
{% if git_hosting == "github" %}- CI via GitHub Actions (NERC-CEH/dri-cicd reusable workflows)
{% endif %}{% if cookiecutter.docs_type == "sphinx" %}- Docs site with Sphinx + Shibuya theme{% if git_hosting == "github" %}, auto-deployed to GitHub Pages{% endif %}
{% endif %}- `Makefile` with dev commands: qa, test, type-check, bump, release
- Pre-commit git hook for ruff format and lint
- Contributing guide, code of conduct
- .editorconfig, .gitignore

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [NERC-CEH/fdri-cookiecutter-pypackage](https://github.com/NERC-CEH/fdri-cookiecutter-pypackage) template.
