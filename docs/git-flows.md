# Git flows and branch protection

## Choosing a git flow

The `git_flow` prompt controls the branching strategy used by the generated project. Choose based on how much overhead
makes sense:

| Option         | Best for                                                              | Branches                              | Branch protection                   |
|----------------|-----------------------------------------------------------------------|---------------------------------------|-------------------------------------|
| `simple`       | One-off scripts, personal tools, early exploration                    | `main` only                           | None                                |
| `github_flow`  | Internal tools, small team projects                                   | `main` + feature branches             | `main` protected                    |
| `main_develop` | PyPI-published libraries, projects with a stable/released distinction | `main` + `develop` + feature branches | Both `main` and `develop` protected |

**Recommendation:** use `main_develop` when `publish_to_pypi=yes`. It keeps `main` exactly in sync with what is on
PyPI - users landing on the GitHub repo see the released version, not work-in-progress code. For everything else,
`github_flow` gives PR-based discipline without the extra branch, and `simple` is fine for solo or exploratory work.

## Branch protection

### GitHub

When `git_flow` is `github_flow` or `main_develop`, the post-generation hook automatically configures branch
protection on `main` (and `develop` for `main_develop`) via `gh api`. The rules applied are:

- **Require a pull request** - no direct pushes to protected branches.
- **1 approving review** - at least one reviewer must approve before merge.
- **CI must pass** - the `test-python` check (and `build-docs` if `docs_type=sphinx`) must be green.
- **Conversations must be resolved** - all review comments must be addressed before merge.

To see the current rules on a branch:

```bash
gh api repos/{owner}/{repo}/branches/main/protection
```

### Codeberg

Branch protection is not configured automatically on the Codeberg path (no CLI equivalent). You can set it up
manually via your repo's **Settings -> Branches** on codeberg.org after pushing.
