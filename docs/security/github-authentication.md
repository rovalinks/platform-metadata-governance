# GitHub Authentication

## Authentication Method

GitHub Actions authenticates using OpenID Connect (OIDC).

Google Cloud exchanges the OIDC token using Workload Identity Federation.

The authenticated workflow impersonates the GitHub Actions service account.

## Security Benefits

- No JSON service account keys
- Short-lived credentials
- Repository-level trust
- Least privilege