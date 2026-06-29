# Workload Identity Module

## Purpose

Creates Google Cloud Workload Identity Federation resources used to authenticate GitHub Actions without service account keys.

## Resources

* Workload Identity Pool
* OIDC Provider
* Service Account IAM Binding

## Authentication Flow

GitHub Actions

↓

GitHub OIDC Token

↓

Workload Identity Pool

↓

OIDC Provider

↓

GitHub Actions Service Account

↓

Google Cloud APIs

## Security

- GitHub authenticates using OpenID Connect (OIDC).
- No service account keys are created or stored.
- Access is restricted to the configured GitHub organisation.
- Service account impersonation uses `roles/iam.workloadIdentityUser`.