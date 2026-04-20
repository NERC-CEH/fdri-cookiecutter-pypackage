.. _index:

:layout: landing

{{ "=" * cookiecutter.project_name | length }}
{{ cookiecutter.project_name }}
{{ "=" * cookiecutter.project_name | length }}

.. rst-class:: lead

    {{ cookiecutter.project_short_description }}

Current version: |release|

.. container:: buttons

    `Docs <installation.html>`_
{% if cookiecutter.git_hosting == "github" %}    `GitHub <https://github.com/{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}>`_
{% elif cookiecutter.git_hosting == "codeberg" %}    `Codeberg <https://codeberg.org/{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}>`_
{% endif %}
Community
=========

Developed at `UKCEH <https://www.ceh.ac.uk/>`_, welcoming community engagement and contributions.

{% if cookiecutter.git_hosting == "github" %}.. contributors:: {{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}
    :avatars:

{% endif %}License
=======

{% if cookiecutter.git_hosting == "github" %}This project is licensed under the `{{ cookiecutter.license }} <https://github.com/{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}/blob/main/LICENSE>`_.
{% elif cookiecutter.git_hosting == "codeberg" %}This project is licensed under the `{{ cookiecutter.license }} <https://codeberg.org/{{ cookiecutter.repo_owner }}/{{ cookiecutter.package_name }}/raw/branch/main/LICENSE>`_.
{% else %}This project is licensed under the {{ cookiecutter.license }}.
{% endif %}

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Getting started

    installation

.. toctree::
    :hidden:
    :maxdepth: 1
    :caption: API reference

    api
