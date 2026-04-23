# Git flow

pyservice uses a fixed `main -> staging -> production` branching model.

## Branches

| Branch       | Triggered by                                              |
|--------------|-----------------------------------------------------------|
| `main`       | PR merge to `main`                                        |
| `staging`    | Auto-PR from `main` after successful deploy to current    |
| `production` | Auto-PR from `staging` after successful deploy to staging |

## How promotion works

1. You merge a PR into `main`. The pipeline runs tests, then builds and deploys the Docker image to the current
environment.
2. On success, the pipeline automatically opens a PR from `main` -> `staging`.
3. After that PR is reviewed and merged, the pipeline deploys to staging and automatically opens a PR
from `staging` -> `production`.
4. After that PR is merged, the pipeline deploys to production.

Branch protection on all three branches requires 1 approving review and passing CI before a merge is allowed.

## Working on a feature

```bash
git checkout -b feature/my-feature   # branch off main
# ... make changes ...
git push -u origin feature/my-feature
gh pr create --base main
```

Never commit directly to `main`, `staging`, or `production`.
