# Terraform Infrastructure

## Purpose

This directory contains the Infrastructure as Code (IaC) used to provision the Metadata Governance Platform on Google Cloud.

Terraform is used to provision and manage all platform infrastructure using the Google Cloud Terraform Provider.

## Remote State

Terraform state is stored remotely in a Google Cloud Storage bucket.

Backend:

* Google Cloud Storage (GCS)

Bucket:

* `platform-metadata-demo-tfstate`

State locking is handled automatically by the GCS backend.

## Provider

* hashicorp/google (v7.x)

## Current Modules

| Module            | Status | Purpose                                                                                    |
| ----------------- | ------ | ------------------------------------------------------------------------------------------ |
| artifact-registry | ✅      | Creates the Artifact Registry repository used to store Governance Engine container images. |
| service-accounts  | ✅      | Creates platform service accounts.                                                         |
| iam               | ✅      | Assigns IAM roles to service accounts.                                                     |
| cloud-run         | 🚧     | Deploys the Governance Engine to Cloud Run.                                                |
| workload-identity | 🚧     | Configures GitHub OIDC authentication using Workload Identity Federation.                  |

## Deployment Order

1. Terraform Backend
2. Artifact Registry
3. Service Accounts
4. IAM
5. Workload Identity Federation
6. Cloud Build
7. Cloud Run
8. Cloud Asset Inventory
9. Eventarc

## Design Principles

* No hardcoded resource identifiers inside modules
* Reusable Terraform modules
* Least privilege IAM
* Google Cloud native services
* Remote state stored in GCS
* Modular Infrastructure as Code

## Modules

- artifact-registry
- service-accounts
- iam
- workload-identity
- cloud-build-trigger
- cloud-run

## GitHub Actions

The GitHub Actions service account must be granted the required IAM roles defined in `terraform.tfvars`.

These permissions are required for Cloud Build submission and Cloud Run deployment.