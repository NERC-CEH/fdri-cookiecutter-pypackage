"""Top-level package for {{ cookiecutter.project_name }}."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("{{ cookiecutter.package_name }}")
except PackageNotFoundError:
    __version__ = "unknown"
