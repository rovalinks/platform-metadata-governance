## Current Progress

### Sprint 1 - Foundation ✅

- Terraform Backend
- Validation Framework
- Registry Reader

### Sprint 2 - Platform Infrastructure ✅

- Artifact Registry
- Service Accounts
- IAM
- Workload Identity Federation

### Sprint 3 - Runtime & CI/CD ✅

- Cloud Build
- Cloud Run
- GitHub Actions
- OIDC Authentication

### Sprint 4 - Discovery ✅

- Cloud Asset Inventory Client
- Resource Discovery Service
- Discovery API
- Common Resource Model

### Sprint 5 - Registry ✅

- Application Registry
- JSON Schema
- Registry Validation
- Governance Service

### Sprint 6 - Compliance Engine ✅

- Expected Metadata Model
- Metadata Comparison
- Compliance Evaluation
- Compliance API

### Sprint 7 - Compliance Reporting ✅

- Compliance Summary
- Compliance Dashboard API


### Sprint 8 - Resource Capability Filtering ✅

- Resource Capability Catalogue
- Capability Service
- Label-Capable Resource Filtering

### Sprint 9 - Registry Metadata Model 🚧

- Registry Metadata Builder
- Registry-driven Expected Labels

### Sprint 10 - Resource Adapter Layer 🚧

- Resource Adapter Service
- Compute Adapter
- Storage Adapter

### Sprint 13 - Compute Engine Enforcement 🚧

- Compute Engine Label Update
- Official Compute Engine Client

### Sprint 14 - Generic Enforcement Engine 🚧

- Generic Executor
- Adapter-based Execution

### Sprint 15 - Verification Engine 🚧

- Verification Model
- Verification Service
- Verification API

### Sprint 16 - BigQuery Dataset Enforcement 🚧

- BigQuery Client
- Dataset Metadata Adapter

### Sprint 22 - Centralised Exception Handling

Implemented:

- Centralised Google Cloud exception formatting
- Executor-level exception handling
- Per-resource execution results

### Sprint 23 - API Model Serialization

Implemented:

- ComplianceResult serialization
- ComplianceSummary serialization
- GovernanceReport serialization
- VerificationResult serialization
- Consistent JSON responses across all REST endpoints

### Sprint 24 - Test Framework

- Configured pytest using `pytest.ini`
- Tests automatically resolve Cloud Run modules
- No import path changes required in test files



### Logging

- Shared application logger
- Service-level operational logging
- Cloud Run compatible stdout logging
- Execution and verification lifecycle logging


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