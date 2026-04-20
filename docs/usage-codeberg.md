# Codeberg setup

## Prerequisites

**1. Create a Codeberg account.** Sign up at <https://codeberg.org> and verify your email. Use the same email as
your git identity (`git config --global user.email`) so commits get linked to your profile.

**2. Get access to the org that will own the repo** (if using an org). By default, the template uses `NERC-CEH` as
`repo_owner`. Either ask an existing member to invite you, or set `repo_owner` to your own username when prompted.

**3. Create a personal access token.** The post-generation hook uses this to create the Codeberg repo automatically.
Without it, you'll get manual instructions to run yourself instead - the token is optional but recommended.

To create a token:

1. Log in to Codeberg and go to **Settings -> Applications -> Access Tokens**
   (<https://codeberg.org/user/settings/applications>)
2. Under **Generate New Token**, give it a descriptive name (e.g. `cookiecutter-hook`)
3. Set the expiry as appropriate (or leave blank for no expiry)
4. Select these scopes:
   - `write:repository` - to create and push to repos
   - `write:organization` - only needed if `repo_owner` is an org rather than your personal account
5. Click **Generate Token** and copy it immediately (it won't be shown again)

**4. Set the token in your shell before running cookiecutter:**

```bash
export CODEBERG_TOKEN=your-token-here
```

To avoid re-entering it every session, add the line to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export CODEBERG_TOKEN=your-token-here' >> ~/.bashrc
source ~/.bashrc
```

> **Security note:** keep this token out of version control. It grants write access to your repos.
> Revoke it at any time from **Settings -> Applications -> Access Tokens**.

## Post-generation steps

### With `CODEBERG_TOKEN` set

The hook will:

1. Verify the token is valid
2. Ask whether the Codeberg repo should be public or private
3. Create the repo under `repo_owner/package_name`
4. Initialise git, make the initial commit, and push to `main`
5. If `git_flow=main_develop`: create and push a `develop` branch, then set it as the default via the Forgejo API

### Without `CODEBERG_TOKEN`

The hook initialises git and makes the initial commit locally, then prints the steps to finish setup:

1. Create your repository at <https://codeberg.org/repo/create>
2. Run the `git remote add` and `git push` commands printed by the hook
3. If `git_flow=main_develop`: also push the `develop` branch and set it as the default in the repo's
   **Settings -> Branches**

### Branch protection

Branch protection is not configured automatically. Set it up via your repo's **Settings -> Branches** on
codeberg.org after pushing.

## Releasing

`make release` works on the Codeberg path - it tags, pushes the tag, and prints the URL to create a Codeberg
Release from the web UI. For `main_develop`, running it from `develop` opens a PR instead (uses `CODEBERG_TOKEN`
if set, otherwise prints the URL). See [Releasing](releasing.md) for the full flow.

## Docs

Sphinx docs are built locally only - there is no automated hosted deployment on the Codeberg path.

```bash
make docs-serve  # live-reload server at http://localhost:8000
make docs-build  # one-off static build
```
