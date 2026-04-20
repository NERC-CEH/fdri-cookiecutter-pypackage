# Releasing

## Git host

The release flow is the same regardless of hosting. The difference is what `make release` does at the end:

- **GitHub** - tags, pushes, and creates a GitHub Release with the CHANGELOG as release notes
- **Codeberg** - tags, pushes, and prints the URL to create a Codeberg Release from the web UI
- **none** - creates a local annotated tag only (no remote to push to)


## Branching workflow

The release flow differs depending on which [git flow](git-flows.md) you have chosen:

### simple / github_flow

```bash
# 1. Bump version and create CHANGELOG stub
make bump-patch   # 0.1.0 -> 0.1.1  (or bump-minor / bump-major)

# 2. Fill in CHANGELOG/<version>.md with release notes, then commit and push
git add CHANGELOG/<version>.md
git commit -m "Add release notes for <version>"
git push origin main    # skip for git_hosting=none

# 3. Tag and release
make release
```

### main_develop

```bash
# 1. On develop, bump version and create CHANGELOG stub
git checkout develop && git pull origin develop
make bump-patch

# 2. Fill in CHANGELOG/<version>.md, commit and push
git add CHANGELOG/<version>.md
git commit -m "Add release notes for <version>"
git push origin develop    # skip for git_hosting=none

# 3. Open a release PR - run from develop, does NOT tag yet
make release   # detects you're on develop: opens a PR instead of tagging

# 4. After the PR is merged, create the tag - run from main
git checkout main && git pull origin main
make release   # detects you're on main: tags and releases
```

`make release` detects which branch you're on and does the right thing - PR when on `develop`, tag when on `main`.
This keeps `main` exactly in sync with what is published.

For `git_hosting=none`, step 3 is replaced by `git checkout main && git merge develop`, then step 4 creates a local
tag.

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
