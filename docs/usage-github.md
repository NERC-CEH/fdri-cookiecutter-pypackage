# GitHub setup

## Prerequisites

Skip this page if your machine is already authenticated to GitHub and you can run `gh auth status` without errors.

**1. Create a GitHub account.** Sign up at <https://github.com/signup> and verify your email. Use the same email as
your git identity (`git config --global user.email`) so commits get linked to your profile.

**2. Get access to the org that will own the repo.** By default, the template creates repos under `NERC-CEH`. Ask an
existing member to invite you, or set `repo_owner` to your own account or a different org when prompted.

**3. Install the [`gh` CLI](https://cli.github.com/).** The post-generation hook uses `gh` to create the repo, enable
Pages, and apply branch protection.

```bash
gh --version  # check if already installed
```

If it's missing, install with (on Debian/Ubuntu):

```bash
sudo apt update
sudo apt install gh
```

If `apt` can't find the package (perhaps you're working on an older Linux distro), follow
[GitHub's official install instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md) instead.

**4. Log in with `gh auth login`.** This configures both `gh` and `git` in one go - no SSH keys or personal access
tokens needed for day-to-day work.

```bash
gh auth login
```

When prompted, choose: `GitHub.com` -> `HTTPS` -> `Y` to authenticate git with your GitHub credentials -> `Login with
a web browser`. Paste the one-time code in the browser when asked. Verify with:

```bash
gh auth status
```

You should see a green tick and scopes including at least `repo`, `workflow`, and `read:org`.

### PyPI account

Only needed if you choose `publish_to_pypi=yes`. Register at <https://pypi.org/> and set up a trusted publisher
for your package - the hook will print the exact steps after generation.

**TODO: Add in information about publishing via organisation PyPI**

## Post-generation steps

The hook first runs a preflight check to confirm `gh` is installed, authenticated, has the `repo` and `workflow`
scopes, and (for org-owned repos) that you're a member of the org. If anything is missing it aborts the GitHub
steps - you still get the local project and an initial commit, and can push to GitHub yourself once the issue is fixed.

If the preflight passes, the tool will:

1. Ask whether the GitHub repo should be public or private
2. Create the repo under `repo_owner/package_name`
3. Enable GitHub Pages (source: GitHub Actions)
4. Create a `pypi` environment (if `publish_to_pypi=yes`)
5. Initialise git, make the initial commit, and push to `main`
6. Create and push a `develop` branch, then set it as the default (if `git_flow=main_develop`)
7. Apply branch protection rules to `main` (and `develop`) (if `git_flow` is `github_flow` or `main_develop`)

If `gh` is not available, you'll see manual instructions in the output instead.

See [Branch protection](git-flows.md#branch-protection) for what rules are applied and how to adjust them.

## Enabling GitHub Pages

GitHub Pages is configured to deploy from GitHub Actions. The docs will go live after the first push to `main`
triggers the pipeline.
