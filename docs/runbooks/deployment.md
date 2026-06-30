# Platform Metadata Governance - Deployment Guide

# Overview

<<<<<<< HEAD
This guide describes how to deploy the Platform Metadata Governance solution into a Google Cloud project using Terraform, GitHub Actions, Workload Identity Federation, Artifact Registry, and Cloud Run.

The deployment pipeline is fully automated and does not require long-lived service account keys.

---

# Deployment Architecture

```
Developer
      │
      ▼
Git Push
      │
      ▼
GitHub Actions
      │
      ▼
Workload Identity Federation (OIDC)
      │
      ▼
Docker Build
      │
      ▼
Artifact Registry
      │
      ▼
Cloud Run
```
=======
This document describes how to deploy the Platform Metadata Governance solution into a Google Cloud project using Terraform and GitHub Actions.

---

# Architecture

Deployment pipeline

Developer
↓

Git Push
↓

GitHub Actions

↓

Workload Identity Federation (OIDC)

↓

Docker Build

↓

Artifact Registry

↓

Cloud Run

No long-lived service account keys are used.
>>>>>>> 649cfac5f0154a8468ffb6b68da077cb026083db

---

# Prerequisites

<<<<<<< HEAD
## Required Software

Install the following tools:

- Git
- Terraform
- Google Cloud CLI (gcloud)
- Docker

---

## Required Google Cloud APIs

Enable the following APIs:

- Artifact Registry API
- Cloud Asset API
- Cloud Run Admin API
- IAM API
- IAM Credentials API
- Cloud Resource Manager API
- Service Usage API

Terraform will require these APIs to be enabled before deployment.

---

# Clone the Repository
=======
## Google Cloud APIs

Enable:

- Artifact Registry API
- Cloud Asset API
- Cloud Run Admin API
- IAM API
- IAM Credentials API
- Resource Manager API
- Service Usage API

---

## GitHub

Fork or clone the repository.

---

## Terraform

Install Terraform.
>>>>>>> 649cfac5f0154a8468ffb6b68da077cb026083db

---

## Google Cloud CLI

Install gcloud CLI.

Authenticate.

---

# Configure Terraform

<<<<<<< HEAD
Copy the example configuration.
=======
Copy
>>>>>>> 649cfac5f0154a8468ffb6b68da077cb026083db

terraform.tfvars.example

↓

terraform.tfvars

Update the following values:

- project_id
- region
<<<<<<< HEAD
- artifact_registry_repository
=======
>>>>>>> 649cfac5f0154a8468ffb6b68da077cb026083db
- GitHub owner
- GitHub repository

Example:

```hcl
project_id = "my-gcp-project"

region = "europe-west2"

artifact_registry_repository = "platform-images"

workload_identity = {

  pool_id = "github-pool"

  provider_id = "github-provider"

  github_owner = "my-github-org"

  github_repository = "platform-metadata-governance"

}
```

---

# Deploy Infrastructure

<<<<<<< HEAD
Deploy the Google Cloud infrastructure.

```bash
=======
>>>>>>> 649cfac5f0154a8468ffb6b68da077cb026083db
cd terraform

terraform init

terraform plan

terraform apply

Terraform provisions:

- Artifact Registry
- Service Accounts
<<<<<<< HEAD
- IAM Roles
- Workload Identity Federation
- Cloud Run Service
=======
- IAM
- Workload Identity Federation
- Cloud Run
>>>>>>> 649cfac5f0154a8468ffb6b68da077cb026083db

---

# Configure GitHub Secrets

<<<<<<< HEAD
Open

Settings

↓

Secrets and Variables

↓

Actions

Create the following secrets.

| Secret | Description |
|---------|-------------|
| WIF_PROVIDER | Full Workload Identity Provider resource name |
| WIF_SERVICE_ACCOUNT | GitHub Actions service account email |

Example

```
WIF_PROVIDER

projects/123456789/locations/global/workloadIdentityPools/github-pool/providers/github-provider
```

```
WIF_SERVICE_ACCOUNT

github-actions-sa@my-project.iam.gserviceaccount.com
```
=======
Create:

| Secret | Description |
|----------|-------------|
| WIF_PROVIDER | Workload Identity Provider |
| WIF_SERVICE_ACCOUNT | GitHub Actions Service Account |
>>>>>>> 649cfac5f0154a8468ffb6b68da077cb026083db

---

# GitHub Actions Deployment

<<<<<<< HEAD
Deployment is fully automated.

Whenever code is merged into the **main** branch:

1. GitHub Actions authenticates using Workload Identity Federation.
2. Docker builds the application image.
3. The image is pushed to Artifact Registry.
4. Cloud Run is updated with the new image.

No manual deployment steps are required.

---

# Registry Governance Workflow

New applications are onboarded using registry files.

Developer creates:

```
registry/applications/APP000002.yaml
```

Workflow:

```
Feature Branch

↓

Git Push

↓

Registry Validation

↓

Pull Request

↓

Approval

↓

Merge to main

↓

Automatic Deployment

↓

Platform Metadata Governance
```

No Python code changes are required when onboarding new applications.
=======
Push to main.

GitHub Actions will:

1. Authenticate using Workload Identity Federation.
2. Build the Docker image.
3. Push the image to Artifact Registry.
4. Deploy Cloud Run.
>>>>>>> 649cfac5f0154a8468ffb6b68da077cb026083db

---

# Verify

<<<<<<< HEAD
After deployment, verify the following endpoints.

| Endpoint | Description |
|----------|-------------|
| GET /health | Service health |
| GET /discover | Resource discovery |
| GET /compliance | Compliance evaluation |
| GET /verify | Metadata verification |
| GET /enforce | Label enforcement |
| GET /report | Governance reporting |

Example:

```text
https://<cloud-run-url>/health
```

---

# Updating the Platform

To deploy new application code:

```bash
git checkout -b feature/my-change

git add .

git commit -m "Describe change"

git push origin feature/my-change
```

Create a Pull Request.

After approval and merge into **main**, GitHub Actions automatically deploys the new version.

---

# Destroy Infrastructure

To remove the deployed infrastructure:

```bash
cd terraform

terraform destroy
```

> **Note**
>
> Google Cloud Workload Identity Pools use a soft-delete lifecycle. If a pool is deleted, its identifier remains reserved for a retention period. Recreating a pool with the same ID immediately after deletion may return a `409 Requested entity already exists` error. During development or testing, either restore the deleted pool or use a new pool ID. This is expected Google Cloud behaviour.

---

# Security

The platform follows Google Cloud security best practices.

- No service account keys are stored in GitHub.
- Authentication uses Workload Identity Federation (OIDC).
- Service accounts follow the principle of least privilege.
- Registry changes require Pull Request approval.
- Registry files are validated before merging.
- Deployments occur only after successful validation and approval.

---

# Deployment Summary

The deployment process is fully automated.

```
Terraform

↓

Google Cloud Infrastructure

↓

GitHub Push

↓

GitHub Actions

↓

Workload Identity Federation

↓

Docker Build

↓

Artifact Registry

↓

Cloud Run

↓

Platform Metadata Governance
```
=======
Verify:

GET /health

GET /discover

GET /compliance

GET /verify

GET /enforce

GET /report

---

# Remove Infrastructure

cd terraform

terraform destroy
>>>>>>> 649cfac5f0154a8468ffb6b68da077cb026083db
