# Releasing

pyservice has no PyPI publishing. A "release" means a new version is deployed to production via the normal promotion flow.

## Bumping the version

```bash
make bump-patch   # 0.1.0 -> 0.1.1
make bump-minor   # 0.1.0 -> 0.2.0
make bump-major   # 0.1.0 -> 1.0.0
```

Each command:

1. Bumps the version in `pyproject.toml`
2. Creates a CHANGELOG stub at `CHANGELOG/<new_version>.md`
3. Commits both with a standard message

Fill in the CHANGELOG stub before opening your PR.

## Deploying to production

Deployment is triggered by merging through the branch chain - there is no separate release script.

1. Merge your feature PR into `main` - deploys to the current environment
2. Review and merge the auto-PR `main -> staging` - deploys to staging
3. Review and merge the auto-PR `staging -> production` - deploys to production

Tag the commit on `main` after it reaches production if you want a named checkpoint:

```bash
git tag v<version>
git push origin v<version>
```
