# Metadata Governance Engine

## Runtime

- Cloud Run
- Flask

## Responsibilities

- Registry Reader
- Cloud Asset Inventory Integration
- Resource Discovery
- Governance Evaluation
- Compliance Evaluation


---

## Runtime Components

### Clients

- Cloud Asset Inventory Client

### Services

### Services

- Governance Service
- Resource Discovery
- Compliance Evaluation

### Handlers

- Health
- Discovery
- Compliance

### Models

- Resource
- Compliance Result

---

## Endpoints

### GET /

Returns service health.

### GET /health

Returns service status and registered applications.

### GET /discover

Returns resources discovered using Google Cloud Asset Inventory.

### GET /compliance

Returns governance results by comparing discovered resources against the Metadata Registry.