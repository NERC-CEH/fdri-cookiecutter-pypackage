# Releasing

A "release" means tagging a version and creating a GitHub Release (or Codeberg/local tag depending on hosting).

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

## Auto-release (if `auto_release=yes`, GitHub only)

If you chose `auto_release=yes`, releases are fully automated - no manual `make release` needed.

The generated project includes two workflows:

- **`release-ready` job** (in `pipeline.yml`) - runs on every PR targeting `main`. If the branch contains a version bump, it checks that `CHANGELOG/<version>.md` exists and is filled in. Blocks the PR if the changelog is missing or still a stub. PRs without a version bump pass unconditionally.
- **`release` job** (in `pipeline.yml`) - runs on every push to `main`. Tags the commit, pushes the tag, and creates a GitHub Release using the changelog as release notes.

The branch protection rules applied during project generation include `release-ready` as a required status check.

**Workflow:**

```bash
# 1. On a branch - bump version and write changelog
make bump-patch   # or bump-minor / bump-major
# Fill in CHANGELOG/<version>.md, commit, and open a PR as normal

# 2. After the PR is merged to main - the release workflow runs automatically
```

## Manual release (if `auto_release=no`)

The release flow depends on which [git flow](git-flows.md) you chose, and what `make release` does varies by hosting:

- **GitHub** - tags, pushes, and creates a GitHub Release with the CHANGELOG as release notes
- **Codeberg** - tags, pushes, and prints the URL to create a Codeberg Release from the web UI
- **none** - creates a local annotated tag only

### simple / github_flow

```bash
# 1. Bump version and write changelog (on a branch)
make bump-patch   # or bump-minor / bump-major
git add CHANGELOG/<version>.md
git commit -m "Add release notes for <version>"
git push origin <branch>

# 2. Merge the PR, then tag and release from main
git checkout main && git pull origin main
make release
```

### main_develop

```bash
# 1. On develop, bump version and write changelog
git checkout develop && git pull origin develop
make bump-patch
git add CHANGELOG/<version>.md
git commit -m "Add release notes for <version>"
git push origin develop

# 2. Open a release PR - run from develop, does NOT tag yet
make release   # detects you're on develop: opens a PR to main instead of tagging

# 3. After the PR is merged, create the tag from main
git checkout main && git pull origin main
make release   # detects you're on main: tags and releases
```

For `git_hosting=none`, step 2 is replaced by `git checkout main && git merge develop`, then step 3 creates a local tag.

---

## Publishing to PyPI (GitHub only)

If `publish_to_pypi=yes`, the pushed tag triggers the `publish.yml` CI workflow, which builds the package and
publishes to PyPI automatically via trusted publishing (no API tokens needed).

**TODO: Add in information about publishing via organisation PyPI**

The post-generation hook prints instructions for adding a trusted publisher on PyPI. Do this once before your
first release:

1. Go to <https://pypi.org/manage/account/publishing/>
2. Fill in the values the hook printed (repo name, owner, workflow: `publish.yml`, environment: `pypi`)
3. From then on, `make release` handles everything - no tokens to manage
