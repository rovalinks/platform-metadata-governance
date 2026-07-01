# Platform Metadata Governance

A cloud-native metadata governance platform for Google Cloud that discovers resources, evaluates compliance against a central application registry, automatically remediates supported resources, and provides governance reporting.

The platform is designed using Google Cloud managed services and follows Infrastructure as Code, GitOps, and Zero Trust authentication principles.

---

# Features

- Registry-driven governance
- Cloud Asset Inventory resource discovery
- Metadata compliance evaluation
- Registry-based expected metadata generation
- Automated metadata enforcement
- Metadata verification
- Governance reporting
- GitHub Pull Request validation
- Infrastructure as Code using Terraform
- Workload Identity Federation
- Cloud Run deployment
- Unit tested business services

---

# Architecture

```
                    +----------------------+
                    |  Application Registry|
                    |  APP000001.yaml      |
                    |  APP000002.yaml      |
                    +----------+-----------+
                               |
                               v
                  +---------------------------+
                  |   Governance Service      |
                  +---------------------------+
                               |
         +---------------------+---------------------+
         |                     |                     |
         v                     v                     v
  Discovery Service     Compliance Service   Enforcement Service
         |                     |                     |
         +----------+----------+----------+----------+
                    |                     |
                    v                     v
           Cloud Asset Inventory     Adapter Layer
                                           |
                     +---------------------+----------------------+
                     |                                            |
                     v                                            v
              Compute Engine                              BigQuery Dataset
```

---

# Repository Structure

```
platform-metadata-governance/

├── cloudrun/
│   ├── clients/
│   ├── handlers/
│   ├── models/
│   ├── registry/
│   ├── services/
│   ├── utils/
│   ├── app.py
│   └── Dockerfile
│
├── registry/
│   ├── applications/
│   └── schemas/
│
├── terraform/
│
├── validation/
│
├── tests/
│
└── docs/
```

---

# Components

## Registry

Contains application metadata.

Each application is defined in an individual YAML file.

Example

```
registry/applications/APP000001.yaml
```

---

## Discovery

Uses Cloud Asset Inventory to discover supported Google Cloud resources.

Currently supported:

- Compute Engine
- BigQuery Dataset
- Cloud Storage (discovery)
- Artifact Registry (discovery)

---

## Governance

Builds the expected metadata model from the Application Registry.

Produces:

- application
- owner
- team
- budgetowner
- organization
- department
- costcenter
- environment
- businesscriticality

---

## Compliance

Compares discovered metadata against registry metadata.

Determines

- compliant
- missing labels
- incorrect labels

---

## Enforcement

Creates remediation plans.

Delegates execution through adapters.

Currently supports

- Compute Engine labels
- BigQuery Dataset labels

---

## Verification

Verifies metadata after remediation.

---

## Reporting

Produces governance summary including

- Total resources
- Supported resources
- Compliant resources
- Non-compliant resources
- Enforcement candidates
- Compliance percentage

---

# REST APIs

| Endpoint | Description |
|----------|-------------|
| GET /health | Platform health |
| GET /discover | Resource discovery |
| GET /compliance | Compliance evaluation |
| GET /verify | Metadata verification |
| GET /enforce | Metadata enforcement |
| GET /report | Governance reporting |

---

# Technology Stack

Infrastructure

- Terraform

Runtime

- Cloud Run
- Flask

Google Cloud Services

- Cloud Asset Inventory
- Artifact Registry
- Cloud Run
- IAM
- Workload Identity Federation

CI/CD

- GitHub Actions
- GitHub Pull Requests

Testing

- Pytest

---

# Security

The platform follows Google Cloud security best practices.

- Workload Identity Federation
- No service account keys
- Least privilege IAM
- Pull Request approval
- Registry validation
- Infrastructure as Code

---

# Deployment

See

```
docs/runbooks/deployment.md
```

---

# Customer Onboarding

See

```
docs/runbooks/customer-onboarding.md
```

---

# API Documentation

See

```
docs/api/API.md
```

---

# Architecture

See

```
docs/architecture/platform-architecture.md
```

---

# Testing

Run all unit tests

```bash
pytest
```

---

# Current Status

| Feature | Status |
|----------|--------|
| Registry | ✅ |
| Validation | ✅ |
| Discovery | ✅ |
| Governance | ✅ |
| Compliance | ✅ |
| Enforcement | ✅ |
| Verification | ✅ |
| Reporting | ✅ |
| Terraform | ✅ |
| GitHub Actions | ✅ |
| Workload Identity Federation | ✅ |

---

# Future Enhancements

- Eventarc automatic enforcement
- Cloud Scheduler
- Cloud Monitoring
- Alerting
- Additional Google Cloud resource adapters