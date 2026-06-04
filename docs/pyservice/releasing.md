# Releasing

pyservice has no PyPI publishing. A "release" means a new version is deployed to production and optionally tagged as a GitHub Release.

## Bumping the version

```bash
make bump-patch   # 0.1.0 -> 0.1.1
make bump-minor   # 0.1.0 -> 0.2.0
make bump-major   # 0.1.0 -> 1.0.0
```

Each command:

1. Bumps the version in `pyproject.toml`
2. Runs `uv lock` to update the lockfile
3. Commits `pyproject.toml` and `uv.lock` (and `CITATION.cff` if present) with a standard message
4. Creates a CHANGELOG stub at `CHANGELOG/<new_version>.md` and commits it separately

Fill in the CHANGELOG stub before opening your PR.

## Deploying to production

Deployment is triggered by merging through the branch chain - there is no separate release script.

1. Merge your feature PR into `staging` - deploys to staging
2. Review and merge the auto-PR `staging -> production` - deploys to production

## Auto-release (if `auto_release=yes`)

If you chose `auto_release=yes`, a GitHub Release is created automatically on every merge to `production`.

The generated project includes two workflows:

- **`release-ready` job** (in `pipeline.yml`) - runs on PRs targeting `production`. If the branch contains a version bump, it checks that `CHANGELOG/<version>.md` exists and is filled in. Blocks the PR if the changelog is missing or still a stub.
- **`release` job** (in `pipeline.yml`) - runs on push to `production`. Tags the commit, pushes the tag, and creates a GitHub Release using the changelog as release notes.

The branch protection rules applied during project generation include `release-ready` as a required status check.

**Workflow:**

```bash
# 1. On a branch - bump version and write changelog
make bump-patch   # or bump-minor / bump-major
# Fill in CHANGELOG/<version>.md, commit, and open a PR to staging as normal

# 2. Once merged to staging and promoted to production - the release workflow runs automatically
```

## Manual release (if `auto_release=no`)

```bash
# After your changes reach production
git checkout production && git pull origin production
make release
```

This tags the commit, pushes the tag, and creates a GitHub Release using the changelog as release notes.
