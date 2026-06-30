# Deployment Guide

# Overview

This guide describes how to deploy the Platform Metadata Governance solution into a Google Cloud project.

---

# Prerequisites

## Required APIs

Enable the following Google Cloud APIs:

- Cloud Asset API
- Cloud Build API
- Cloud Run Admin API
- Artifact Registry API
- IAM API
- IAM Credentials API
- Resource Manager API
- Service Usage API

---

# Clone Repository

```bash
git clone <repository-url>

cd platform-metadata-governance
```

---

# Configure Terraform

Copy the example configuration:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Update:

- project_id
- region
- artifact registry
- GitHub owner
- GitHub repository

---

# Deploy Infrastructure

```bash
cd terraform

terraform init

terraform plan

terraform apply
```

Terraform creates:

- Service Accounts
- IAM
- Artifact Registry
- Workload Identity Federation
- Cloud Run
- Cloud Build Trigger

---

# Configure GitHub

Configure the following GitHub Secrets:

| Secret | Description |
|--------|-------------|
| WIF_PROVIDER | Workload Identity Provider resource name |
| WIF_SERVICE_ACCOUNT | GitHub Actions service account |

---

# Deploy Application

Push to the main branch:

```bash
git push origin main
```

GitHub Actions authenticates using Workload Identity Federation and submits the Cloud Build.

---

# Verify Deployment

Verify the following endpoints:

```
GET /health
GET /discover
GET /compliance
GET /verify
GET /enforce
GET /report
```

---

# Cleanup

To remove all infrastructure:

```bash
cd terraform

terraform destroy
```