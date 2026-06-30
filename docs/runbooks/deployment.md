# Platform Metadata Governance - Deployment Guide

# Overview

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

---

# Prerequisites

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

---

## Google Cloud CLI

Install gcloud CLI.

Authenticate.

---

# Configure Terraform

Copy

terraform.tfvars.example

↓

terraform.tfvars

Update:

- project_id
- region
- GitHub owner
- GitHub repository

---

# Deploy Infrastructure

cd terraform

terraform init

terraform plan

terraform apply

Terraform provisions:

- Artifact Registry
- Service Accounts
- IAM
- Workload Identity Federation
- Cloud Run

---

# Configure GitHub Secrets

Create:

| Secret | Description |
|----------|-------------|
| WIF_PROVIDER | Workload Identity Provider |
| WIF_SERVICE_ACCOUNT | GitHub Actions Service Account |

---

# Deploy Application

Push to main.

GitHub Actions will:

1. Authenticate using Workload Identity Federation.
2. Build the Docker image.
3. Push the image to Artifact Registry.
4. Deploy Cloud Run.

---

# Verify

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