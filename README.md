## Current Progress

### Sprint 1 - Foundation ✅

- Terraform Backend
- Artifact Registry
- IAM
- Service Accounts
- Validation Framework
- Registry Reader

### Sprint 2 - In Progress

- Cloud Build
- Cloud Run
- Workload Identity Federation

## Authentication

The platform uses GitHub OpenID Connect (OIDC) with Google Cloud Workload Identity Federation.

No service account keys are stored in GitHub.

## CI/CD Authentication

The platform authenticates GitHub Actions to Google Cloud using:

- GitHub OpenID Connect (OIDC)
- Google Cloud Workload Identity Federation
- Service Account Impersonation

No long-lived service account keys are used.