## Current Progress

### Sprint 1 - Foundation ✅

- Terraform Backend
- Artifact Registry
- IAM
- Service Accounts
- Validation Framework
- Registry Reader

### Sprint 2 - Platform Infrastructure ✅

- Artifact Registry
- Service Accounts
- IAM
- Cloud Build
- Workload Identity Federation

### Sprint 3 - CI/CD ✅

- GitHub Actions
- Cloud Build
- Artifact Registry
- Workload Identity Federation
- Immutable image tagging

## Authentication

The platform uses GitHub OpenID Connect (OIDC) with Google Cloud Workload Identity Federation.

No service account keys are stored in GitHub.

## Platform Identities

| Service Account      | Purpose                                                                     |
| -------------------- | --------------------------------------------------------------------------- |
| terraform-sa         | Provisions and manages Google Cloud infrastructure using Terraform.         |
| governance-engine-sa | Runtime identity for the Metadata Governance Engine running on Cloud Run.   |
| github-actions-sa    | Identity impersonated by GitHub Actions using Workload Identity Federation. |
| cloud-build-sa       | Executes Cloud Build jobs and pushes container images to Artifact Registry. |

Each identity follows the principle of least privilege and has a dedicated responsibility.


## CI/CD Authentication

The platform authenticates GitHub Actions to Google Cloud using:

- GitHub OpenID Connect (OIDC)
- Google Cloud Workload Identity Federation
- Service Account Impersonation

No long-lived service account keys are used.


## Deployment

The platform uses GitHub Actions with Google Cloud Workload Identity Federation.

Deployment flow:

Git Push

↓

GitHub Actions

↓

OIDC Authentication

↓

Cloud Build

↓

Artifact Registry

↓

Cloud Run

No service account keys are stored in GitHub.


## Continuous Integration

The platform uses GitHub Actions with Workload Identity Federation.

Workflow:

Git Push

↓

GitHub Actions

↓

Google Workload Identity Federation

↓

Cloud Build

↓

Artifact Registry

Container images are tagged using the Git commit SHA.