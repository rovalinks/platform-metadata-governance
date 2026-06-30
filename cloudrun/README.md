# Metadata Governance Engine

## Runtime

- Cloud Run
- Flask

## Responsibilities

- Registry Reader
- Governance Service
- Resource Discovery Service
- Capability Service
- Metadata Compliance Engine
- Metadata Enforcement Planner


---

## Runtime Components

## Clients

- Cloud Asset Inventory Client
- Compute Client
- Storage Client

## Services

- Governance Service
- Discovery Service
- Capability Service
- Compliance Service
- Enforcement Service

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