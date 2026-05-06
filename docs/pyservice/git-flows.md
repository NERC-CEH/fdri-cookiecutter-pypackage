# Git flow

pyservice uses a fixed `staging -> production` branching model.

## Branches

| Branch       | Triggered by                                              |
|--------------|-----------------------------------------------------------|
| `staging`    | PR merge to `staging`                                     |
| `production` | Auto-PR from `staging` after successful deploy to staging |

## How promotion works

1. You merge a feature PR into `staging`. The pipeline runs tests, then builds and deploys the Docker image to the
staging environment.
2. On success, the pipeline automatically opens a PR from `staging` -> `production`.
3. After that PR is reviewed and merged, the pipeline deploys to production.

Branch protection on both branches requires 1 approving review and passing CI before a merge is allowed.

## Working on a feature

```bash
git checkout staging
git pull origin staging
git checkout -b feature/my-feature
# ... make changes ...
git push -u origin feature/my-feature
gh pr create --base staging
```

Never commit directly to `staging` or `production`.