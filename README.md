# Platform Metadata Governance

## Overview

Platform Metadata Governance is a registry-driven metadata governance platform for Google Cloud.

The platform discovers cloud resources using Cloud Asset Inventory, compares them against a centrally managed application registry, evaluates metadata compliance, and automatically applies metadata to supported resources.

Current supported enforcement targets:

- Compute Engine Instances
- BigQuery Datasets

---

## Project Progress

### Completed

#### Sprint 1 - Foundation
- Terraform backend
- Registry reader
- Validation framework

#### Sprint 2 - Platform Infrastructure
- Artifact Registry
- Service Accounts
- IAM
- Workload Identity Federation

#### Sprint 3 - Runtime & CI/CD
- Cloud Build
- Cloud Run
- GitHub Actions
- GitHub OIDC Authentication

#### Sprint 4 - Discovery
- Cloud Asset Inventory client
- Discovery service
- Discovery API
- Common resource model

#### Sprint 5 - Registry
- Application registry
- JSON Schema validation
- Registry validation
- Governance service

#### Sprint 6 - Compliance Engine
- Expected metadata model
- Compliance evaluation
- Compliance API

#### Sprint 7 - Compliance Reporting
- Compliance summary
- Governance reporting API

#### Sprint 8 - Capability Filtering
- Resource capability catalogue
- Capability service
- Supported resource filtering

#### Sprint 9 - Registry Metadata
- Registry-driven metadata model
- Registry-driven expected labels

#### Sprint 10 - Resource Adapter Layer
- Adapter framework
- Compute adapter
- BigQuery adapter

#### Sprint 11 - Enforcement Engine
- Generic enforcement engine
- Generic executor
- Adapter-based execution

#### Sprint 12 - Verification
- Verification service
- Verification API
- Verification model

#### Sprint 13 - Compute Engine Enforcement
- Compute Engine label enforcement
- Official Google Cloud Compute client

#### Sprint 14 - BigQuery Dataset Enforcement
- BigQuery Dataset label enforcement
- Official BigQuery client

#### Sprint 15 - Production Hardening
- Centralised logging
- Centralised exception handling
- API model serialization
- Unit testing
- Pytest configuration

---

## Configuration

The repository includes a complete `terraform.tfvars.example` file.

Create your own configuration by copying:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars