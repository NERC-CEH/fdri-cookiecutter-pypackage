# GitHub and AWS setup

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

### GitHub org membership

By default the service is created under `NERC-CEH`. Ask an existing member to invite you, or set `repo_owner` to
your own account when prompted.

### AWS OIDC roles

The pipeline deploys Docker images to three environments using AWS OIDC. Before the
first deployment succeeds you need four IAM roles - one per environment plus the region:

| Secret                    | What it is                                       |
|---------------------------|--------------------------------------------------|
| `AWS_REGION`              | AWS region, e.g. `eu-west-2`                     |
| `AWS_ROLE_ARN`            | OIDC role for the **current** (main) environment |
| `AWS_ROLE_ARN_STAGING`    | OIDC role for the **staging** environment        |
| `AWS_ROLE_ARN_PRODUCTION` | OIDC role for the **production** environment     |

Ask an admin for the correct details for your service. See the [dri-cicd docs](https://github.com/NERC-CEH/dri-cicd)
for more information.

## What the hook does

After generation, the hook:

1. Checks `gh` is installed, authenticated, and has the required scopes
2. Asks whether the repo should be public or private
3. Creates the GitHub repo under `repo_owner/package_name`
4. Enables GitHub Pages
5. Initialises git and makes the initial commit
6. Creates `staging` and `production` branches, then pushes all three (`main`, `staging`, `production`) to GitHub
7. Applies branch protection to all three branches (requires 1 approving review + passing CI)

If `gh` is not available, you get the local project and initial commit but must push manually.

## AWS secrets

After the repo is created, add the four secrets before merging anything to `main`:

1. Go to `https://github.com/<repo_owner>/<package_name>/settings/secrets/actions`
2. Add each of the four secrets listed above

The pipeline will fail on any push to `main`, `staging`, or `production` until these are present.

## GitHub Pages

Pages is configured to deploy from GitHub Actions. Docs go live after the first push to `main` triggers the pipeline.
