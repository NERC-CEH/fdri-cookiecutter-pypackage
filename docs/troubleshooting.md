# Troubleshooting

**`uv: command not found` right after installing uv.** The installer adds uv to a directory that is sourced in
your shell startup script, but the current shell doesn't know about it yet. Start a new terminal, or run
`source ~/.bashrc` (or `source ~/.zshrc`).

**`gh: command not found`.** The `gh` CLI isn't installed or isn't on `PATH`. Re-run the installation step in
[GitHub setup](usage-github.md#prerequisites) and verify with `gh --version`.

**`gh auth status` says "not logged in".** Run `gh auth login` and follow the prompts.

**Preflight says "gh token missing 'workflow' scope".** The hook will open a browser to re-authorise.
If you're using a `GH_TOKEN` environment variable instead, regenerate it with the `workflow` scope at
<https://github.com/settings/tokens> and re-run. You can also refresh manually with:

```bash
gh auth refresh -s workflow
```

**Preflight says "no access to '<org>'".** You don't have membership in the org named in `repo_owner`.
Either ask to be added, or re-run the template and set `repo_owner` to your personal GitHub
username.

**`CODEBERG_TOKEN` check failed (HTTP 401).** The token is invalid or has been revoked. Generate a new one at
<https://codeberg.org/user/settings/applications> - see [Codeberg setup](usage-codeberg.md#prerequisites) for the
required scopes. Re-export it before re-running cookiecutter.

**Codeberg hook says "Could not create repo (HTTP 403)".** The token lacks the `write:organization` scope (needed
when `repo_owner` is an org). Regenerate the token with that scope added, or create the repo manually on Codeberg
and push yourself.

**`make: command not found`.** Install build tools: `sudo apt install build-essential`.

**Commits don't show up under your GitHub profile.** Your local `user.email` doesn't match an email registered
on your GitHub account. Check with `git config --global user.email` and fix via GitHub -> Settings -> Emails, or
change your local config.
