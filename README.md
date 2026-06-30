# Platform Metadata Governance

## Overview

Platform Metadata Governance is a registry-driven metadata governance platform for Google Cloud.

The platform discovers cloud resources using Cloud Asset Inventory, compares them against a centrally managed application registry, evaluates metadata compliance, and automatically applies metadata to supported resources.

Current supported enforcement targets:

- Compute Engine Instances
- BigQuery Datasets

---

# Project Progress

## Completed

### Sprint 1 - Foundation

- Terraform backend
- Registry reader
- Validation framework

### Sprint 2 - Platform Infrastructure

- Artifact Registry
- Service Accounts
- IAM
- Workload Identity Federation

### Sprint 3 - Runtime & CI/CD

- Cloud Build
- Cloud Run
- GitHub Actions
- GitHub OIDC Authentication

### Sprint 4 - Discovery

- Cloud Asset Inventory client
- Discovery service
- Discovery API
- Common resource model

### Sprint 5 - Registry

- Application registry
- JSON Schema validation
- Registry validation
- Governance service

### Sprint 6 - Compliance Engine

- Expected metadata model
- Compliance evaluation
- Compliance API

### Sprint 7 - Compliance Reporting

- Compliance summary
- Governance reporting API

### Sprint 8 - Capability Filtering

- Resource capability catalogue
- Capability service
- Supported resource filtering

### Sprint 9 - Registry Metadata

- Registry-driven metadata model
- Registry-driven expected labels

### Sprint 10 - Resource Adapter Layer

- Adapter framework
- Compute adapter
- BigQuery adapter

### Sprint 11 - Enforcement Engine

- Generic enforcement engine
- Generic executor
- Adapter-based execution

### Sprint 12 - Verification

- Verification service
- Verification API
- Verification model

### Sprint 13 - Compute Engine Enforcement

- Compute Engine label enforcement
- Official Google Cloud Compute client

### Sprint 14 - BigQuery Dataset Enforcement

- BigQuery Dataset label enforcement
- Official BigQuery client

### Sprint 15 - Production Hardening

- Centralised logging
- Centralised exception handling
- API model serialization
- Unit testing
- Pytest configuration


### Registry Validation

The registry enforces:

- JSON Schema validation
- Required fields
- Valid field formats
- Unique `projectId` across all registry files

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


## REST API

| Endpoint | Description |
|----------|-------------|
| GET / | Service information |
| GET /health | Service health |
| GET /discover | Discover supported Google Cloud resources |
| GET /compliance | Evaluate metadata compliance |
| GET /verify | Verify metadata after enforcement |
| GET /enforce | Apply metadata to supported resources |
| GET /report | Governance summary report |

Detailed API documentation is available in:

docs/api/API.md