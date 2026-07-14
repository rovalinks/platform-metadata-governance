# Enterprise Metadata Governance Platform

# Infrastructure Deployment Guide

Version 1.0

---

# Purpose

This document provisions the Google Cloud infrastructure required to host the Enterprise Metadata Governance Platform.

At the end of this guide the following components will exist.

- Google Cloud Project
- Billing
- Required APIs
- Service Accounts
- IAM
- Workload Identity Federation
- Artifact Registry

No application code is deployed in this document.

---

# Deployment Architecture

```
Developer

        │

        ▼

GitHub Repository

        │

        ▼

Workload Identity Federation

        │

        ▼

Google Cloud

        │

        ▼

Artifact Registry

        │

        ▼

Cloud Run
```

---

# Prerequisites

Install

- Google Cloud SDK
- Git
- GitHub CLI (optional)

Authenticate

```bash
gcloud auth login

gcloud auth application-default login
```

---

# Required Variables

```bash
export PROJECT_ID=platform-metadata

export REGION=europe-west2

export SERVICE_ACCOUNT=metadata-governance

export REPOSITORY_NAME=metadata-governance
```

---

# Step 1

Select Project

```bash
gcloud config set project $PROJECT_ID
```

Verify

```bash
gcloud config get-value project
```

---

# Step 2

Verify Billing

```bash
gcloud beta billing projects describe $PROJECT_ID
```

Expected

```
billingEnabled: true
```

---

# Step 3

Enable Required APIs

```bash
gcloud services enable \
artifactregistry.googleapis.com \
bigquery.googleapis.com \
cloudasset.googleapis.com \
cloudbuild.googleapis.com \
cloudresourcemanager.googleapis.com \
eventarc.googleapis.com \
iam.googleapis.com \
iamcredentials.googleapis.com \
logging.googleapis.com \
pubsub.googleapis.com \
run.googleapis.com \
secretmanager.googleapis.com \
serviceusage.googleapis.com \
sqladmin.googleapis.com \
storage.googleapis.com
```

Verify

```bash
gcloud services list --enabled
```

---

# Step 4

Create Runtime Service Account

```bash
gcloud iam service-accounts create metadata-governance \
--display-name="Metadata Governance Platform"
```

Verify

```bash
gcloud iam service-accounts list
```

Expected

```
metadata-governance@$PROJECT_ID.iam.gserviceaccount.com
```

---

# Step 5

Grant Runtime IAM Roles

Grant the runtime service account the required roles.

| Role | Purpose |
|-------|----------|
| Cloud Asset Viewer | Discovery |
| BigQuery Data Editor | Reporting |
| BigQuery Job User | Queries |
| Logging Viewer | Read Audit Logs |
| Pub/Sub Subscriber | Greenfield Processing |
| Storage Admin | Bucket Remediation |
| Compute Admin | VM/Disk Remediation |
| Cloud SQL Admin | Cloud SQL Remediation |
| Secret Manager Admin | Secret Remediation |
| Artifact Registry Admin | Repository Remediation |
| Cloud KMS Admin | Key Remediation |
| Resource Manager Tag User | Apply Tags |
| Resource Manager Tag Viewer | Read Tags |

Apply using:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:metadata-governance@$PROJECT_ID.iam.gserviceaccount.com" \
--role="ROLE_NAME"
```

Repeat for every required role or use 

# Metadata Governance Platform Setup Guide

This guide provides the complete setup steps and scripts to configure your project's IAM permissions, create the BigQuery database in `europe-west2`, and deploy the Eventarc trigger.

---

## 1. Apply IAM Permissions

This script configures the required IAM roles for your Cloud Run, Eventarc, and Cloud Build service accounts.

### File: `apply-iam-permissions.sh`
```bash
#!/usr/bin/env bash

# Exit immediately if any command fails
set -e

# ==========================================
# CONFIGURATION
# ==========================================
PROJECT_ID="platform-metadata"

# Define Service Account Emails
RUN_SA="metadata-governance@${PROJECT_ID}.iam.gserviceaccount.com"
EVENTARC_SA="eventarc-trigger@${PROJECT_ID}.iam.gserviceaccount.com"
CLOUDBUILD_SA="cloudbuild@${PROJECT_ID}.iam.gserviceaccount.com"

echo "Setting up IAM policies for project: ${PROJECT_ID}"

# ==========================================
# 1. CLOUD RUN RUNTIME PERMISSIONS
# ==========================================
echo "Applying Cloud Run runtime roles..."

RUNTIME_ROLES=(
  "roles/cloudasset.viewer"
  "roles/bigquery.jobUser"
  "roles/bigquery.dataEditor"
  "roles/bigquery.dataViewer"
  "roles/resourcemanager.tagUser"
  "roles/resourcemanager.tagViewer"
  "roles/logging.viewer"
  "roles/pubsub.subscriber"
  "roles/pubsub.viewer"
  "roles/storage.admin"
  "roles/compute.admin"
  "roles/cloudsql.admin"
  "roles/artifactregistry.admin"
  "roles/secretmanager.admin"
  "roles/cloudkms.admin"
)

for role in "${RUNTIME_ROLES[@]}"; do
  echo "Granting ${role} to${RUN_SA}..."
  gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${RUN_SA}" \
    --role="${role}" \
    --quiet > /dev/null
done

# ==========================================
# 2. EVENTARC SERVICE ACCOUNT PERMISSIONS
# ==========================================
echo "Applying Eventarc receiver role..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${EVENTARC_SA}" \
  --role="roles/eventarc.eventReceiver" \
  --quiet > /dev/null

# ==========================================
# 3. CLOUD BUILD SERVICE ACCOUNT PERMISSIONS
# ==========================================
echo "Applying Cloud Build roles..."
CLOUDBUILD_ROLES=(
  "roles/cloudbuild.builds.editor"
  "roles/artifactregistry.writer"
)

for role in "${CLOUDBUILD_ROLES[@]}"; do
  echo "Granting ${role} to${CLOUDBUILD_SA}..."
  gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${CLOUDBUILD_SA}" \
    --role="${role}" \
    --quiet > /dev/null
done

echo "IAM policy configuration completed successfully!"


chmod +x apply-iam-permissions.sh
./apply-iam-permissions.sh

---

# Step 6

Configure GitHub Workload Identity Federation

Create Workload Identity Pool

```bash
gcloud iam workload-identity-pools create github \
--location=global \
--display-name="GitHub Actions"
```

Retrieve Project Number

```bash
gcloud projects describe $PROJECT_ID \
--format="value(projectNumber)"
```

Create OIDC Provider

```bash
gcloud iam workload-identity-pools providers create-oidc github \
--location=global \
--workload-identity-pool=github \
--issuer-uri=https://token.actions.githubusercontent.com \
--attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
--attribute-condition="assertion.repository=='YOUR_GITHUB_ORG/YOUR_REPOSITORY'"
```

Allow GitHub to impersonate the runtime service account.

```bash
gcloud iam service-accounts add-iam-policy-binding \
metadata-governance@$PROJECT_ID.iam.gserviceaccount.com \
--role=roles/iam.workloadIdentityUser \
--member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github/attribute.repository/YOUR_GITHUB_ORG/YOUR_REPOSITORY"
```

---

# Step 7

Configure GitHub Secrets

Repository Settings

Secrets and Variables

Actions

Create

| Secret | Value |
|----------|-------|
| WIF_PROVIDER | Workload Identity Provider Resource Name |
| WIF_SERVICE_ACCOUNT | metadata-governance@$PROJECT_ID.iam.gserviceaccount.com |

---

# Step 8

Create Artifact Registry

```bash
gcloud artifacts repositories create metadata-governance \
--repository-format=docker \
--location=$REGION \
--description="Enterprise Metadata Governance Images"
```

Verify

```bash
gcloud artifacts repositories list
```

Expected

```
metadata-governance
```

---

# Infrastructure Validation

Verify

✓ Project configured

✓ Billing enabled

✓ APIs enabled

✓ Runtime Service Account exists

✓ IAM configured

✓ GitHub OIDC configured

✓ Artifact Registry created

Infrastructure deployment is now complete.



# Enterprise Metadata Governance Platform

# Infrastructure Deployment Guide

Version 1.0

---

# Purpose

This document provisions the Google Cloud infrastructure required to host the Enterprise Metadata Governance Platform.

At the end of this guide the following components will exist.

- Google Cloud Project
- Billing
- Required APIs
- Service Accounts
- IAM
- Workload Identity Federation
- Artifact Registry

No application code is deployed in this document.

---

# Deployment Architecture

```
Developer

        │

        ▼

GitHub Repository

        │

        ▼

Workload Identity Federation

        │

        ▼

Google Cloud

        │

        ▼

Artifact Registry

        │

        ▼

Cloud Run
```

---

# Prerequisites

Install

- Google Cloud SDK
- Git
- GitHub CLI (optional)

Authenticate

```bash
gcloud auth login

gcloud auth application-default login
```

---

# Required Variables

```bash
export PROJECT_ID=platform-metadata

export REGION=europe-west2

export SERVICE_ACCOUNT=metadata-governance

export REPOSITORY_NAME=metadata-governance
```

---

# Step 1

Select Project

```bash
gcloud config set project $PROJECT_ID
```

Verify

```bash
gcloud config get-value project
```

---

# Step 2

Verify Billing

```bash
gcloud beta billing projects describe $PROJECT_ID
```

Expected

```
billingEnabled: true
```

---

# Step 3

Enable Required APIs

```bash
gcloud services enable \
artifactregistry.googleapis.com \
bigquery.googleapis.com \
cloudasset.googleapis.com \
cloudbuild.googleapis.com \
cloudresourcemanager.googleapis.com \
eventarc.googleapis.com \
iam.googleapis.com \
iamcredentials.googleapis.com \
logging.googleapis.com \
pubsub.googleapis.com \
run.googleapis.com \
secretmanager.googleapis.com \
serviceusage.googleapis.com \
sqladmin.googleapis.com \
storage.googleapis.com
```

Verify

```bash
gcloud services list --enabled
```

---

# Step 4

Create Runtime Service Account

```bash
gcloud iam service-accounts create metadata-governance \
--display-name="Metadata Governance Platform"
```

Verify

```bash
gcloud iam service-accounts list
```

Expected

```
metadata-governance@$PROJECT_ID.iam.gserviceaccount.com
```

---

# Step 5

Grant Runtime IAM Roles

Grant the runtime service account the required roles.

| Role | Purpose |
|-------|----------|
| Cloud Asset Viewer | Discovery |
| BigQuery Data Editor | Reporting |
| BigQuery Job User | Queries |
| Logging Viewer | Read Audit Logs |
| Pub/Sub Subscriber | Greenfield Processing |
| Storage Admin | Bucket Remediation |
| Compute Admin | VM/Disk Remediation |
| Cloud SQL Admin | Cloud SQL Remediation |
| Secret Manager Admin | Secret Remediation |
| Artifact Registry Admin | Repository Remediation |
| Cloud KMS Admin | Key Remediation |
| Resource Manager Tag User | Apply Tags |
| Resource Manager Tag Viewer | Read Tags |

Apply using:

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:metadata-governance@$PROJECT_ID.iam.gserviceaccount.com" \
--role="ROLE_NAME"
```

Repeat for every required role.

---

# Step 6

Configure GitHub Workload Identity Federation

Create Workload Identity Pool

```bash
gcloud iam workload-identity-pools create github \
--location=global \
--display-name="GitHub Actions"
```

Retrieve Project Number

```bash
gcloud projects describe $PROJECT_ID \
--format="value(projectNumber)"
```

Create OIDC Provider

```bash
gcloud iam workload-identity-pools providers create-oidc github \
--location=global \
--workload-identity-pool=github \
--issuer-uri=https://token.actions.githubusercontent.com \
--attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
--attribute-condition="assertion.repository=='YOUR_GITHUB_ORG/YOUR_REPOSITORY'"
```

Allow GitHub to impersonate the runtime service account.

```bash
gcloud iam service-accounts add-iam-policy-binding \
metadata-governance@$PROJECT_ID.iam.gserviceaccount.com \
--role=roles/iam.workloadIdentityUser \
--member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github/attribute.repository/YOUR_GITHUB_ORG/YOUR_REPOSITORY"
```

---

# Step 7

Configure GitHub Secrets

Repository Settings

Secrets and Variables

Actions

Create

| Secret | Value |
|----------|-------|
| WIF_PROVIDER | Workload Identity Provider Resource Name |
| WIF_SERVICE_ACCOUNT | metadata-governance@$PROJECT_ID.iam.gserviceaccount.com |

---

# Step 8

Create Artifact Registry

```bash
gcloud artifacts repositories create metadata-governance \
--repository-format=docker \
--location=$REGION \
--description="Enterprise Metadata Governance Images"
```

Verify

```bash
gcloud artifacts repositories list
```

Expected

```
metadata-governance
```

---

# Infrastructure Validation

Verify

✓ Project configured

✓ Billing enabled

✓ APIs enabled

✓ Runtime Service Account exists

✓ IAM configured

✓ GitHub OIDC configured

✓ Artifact Registry created

Infrastructure deployment is now complete.


# Enterprise Metadata Governance Platform

# Platform Configuration & Validation Guide

Version 1.0

---

# Purpose

This guide configures the Metadata Governance Platform after the application has been successfully deployed.

At the end of this guide the platform will support:

- BigQuery Reporting
- Brownfield Governance
- Greenfield Governance
- Executive Dashboard
- Organization-level Reporting
- Project-level Reporting

---

# Deployment Order

The platform components must be configured in the following order.

```
Cloud Run

↓

BigQuery Dataset

↓

BigQuery Tables

↓

Governance Registry

↓

Pub/Sub

↓

Logging Sink

↓

Logging Publisher Permissions

↓

Eventarc

↓

Brownfield

↓

Greenfield

↓

Dashboard Validation
```

Do not change this order.

---

# Step 1 - Create BigQuery Dataset

The Metadata Governance Platform stores all reporting information in BigQuery.

Create the dataset.

```bash
bq mk \
--location=$REGION \
metadata_governance_dataset
```

Verify.

```bash
bq ls
```

Expected.

```
metadata_governance_dataset
```

---

# Step 2 - Create Reporting Tables

The platform requires four reporting tables.

| Table | Purpose |
|---------|----------|
| resource_snapshot | Resource inventory |
| compliance_snapshot | Compliance results |
| remediation_plan | Planned remediation |
| remediation_execution | Execution history |

Verify.

```bash
bq ls metadata_governance_dataset
```

Expected.

```
resource_snapshot

compliance_snapshot

remediation_plan

remediation_execution
```

---

# BigQuery Table Definitions

## resource_snapshot

| Column | Type |
|----------|------|
| run_id | STRING |
| snapshot_time | TIMESTAMP |
| project_id | STRING |
| asset_type | STRING |
| resource_name | STRING |
| location | STRING |
| labels | JSON |
| tags | JSON |

---

## compliance_snapshot

| Column | Type |
|----------|------|
| run_id | STRING |
| evaluated_time | TIMESTAMP |
| project_id | STRING |
| asset_type | STRING |
| resource_name | STRING |
| compliant | BOOLEAN |
| missing_labels | JSON |
| incorrect_labels | JSON |

---

## remediation_plan

| Column | Type |
|----------|------|
| remediation_id | STRING |
| run_id | STRING |
| project_id | STRING |
| asset_type | STRING |
| resource_name | STRING |
| status | STRING |
| planned_time | TIMESTAMP |

---

## remediation_execution

| Column | Type |
|----------|------|
| execution_id | STRING |
| run_id | STRING |
| project_id | STRING |
| asset_type | STRING |
| resource_name | STRING |
| status | STRING |
| executed_at | TIMESTAMP |
| error_message | STRING |

---

# Create BigQuery Governance Tables

This guide provides the complete, copy-pasteable script to set up your BigQuery dataset in London (`europe-west2`) and create the four requested governance tables: `resource_snapshot`, `compliance_snapshot`, `remediation_plan`, and `remediation_execution`[cite: 3, 5, 6, 7].

The script is specifically designed to stream the schemas safely using standard input, preventing any unexpected script terminations when running under `set -e`.

---

## 1. The Script

Save the following code block to a file named `create-bq-tables.sh`.

```bash
#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# =====================================================================
# CONFIGURATION
# =====================================================================
PROJECT_ID="platform-metadata"   # Your GCP Project ID
DATASET_ID="metadata_governance" # Your BigQuery Dataset ID
LOCATION="europe-west2"          # London region

echo "Using Project: ${PROJECT_ID}"
echo "Using Dataset: ${DATASET_ID}"
echo "Location:      ${LOCATION}"

# Create the dataset if it does not exist
echo "Ensuring BigQuery dataset '${DATASET_ID}' exists..."
bq show --project_id="${PROJECT_ID}" "${DATASET_ID}" > /dev/null 2>&1 || \
bq --project_id="${PROJECT_ID}" mk --dataset --location="${LOCATION}" "${DATASET_ID}"

# Helper function to read schema from stdin and create the table
create_table() {
  local table_name=$1

  echo "Creating table: ${table_name}..."
  
  # Read schema from stdin and write to a temporary file
  cat > "/tmp/${table_name}_schema.json"
  
  # Create the table using the schema file
  bq --project_id="${PROJECT_ID}" mk \
    --table \
    "${DATASET_ID}.${table_name}" \
    "/tmp/${table_name}_schema.json"

  # Clean up the temp file
  rm "/tmp/${table_name}_schema.json"
}

# =====================================================================
# TABLE 1: resource_snapshot
# =====================================================================
create_table "resource_snapshot" <<'EOF'
[
  {
    "name": "run_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "snapshot_time",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  },
  {
    "name": "project_id",
    "type": "STRING"
  },
  {
    "name": "asset_type",
    "type": "STRING"
  },
  {
    "name": "resource_name",
    "type": "STRING"
  },
  {
    "name": "location",
    "type": "STRING"
  },
  {
    "name": "labels",
    "type": "STRING"
  },
  {
    "name": "tags",
    "type": "STRING"
  }
]
EOF

# =====================================================================
# TABLE 2: compliance_snapshot
# =====================================================================
create_table "compliance_snapshot" <<'EOF'
[
  {
    "name": "run_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "evaluated_time",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  },
  {
    "name": "project_id",
    "type": "STRING"
  },
  {
    "name": "asset_type",
    "type": "STRING"
  },
  {
    "name": "resource_name",
    "type": "STRING"
  },
  {
    "name": "compliant",
    "type": "BOOL"
  },
  {
    "name": "missing_labels",
    "type": "STRING"
  },
  {
    "name": "incorrect_labels",
    "type": "STRING"
  }
]
EOF

# =====================================================================
# TABLE 3: remediation_plan
# =====================================================================
create_table "remediation_plan" <<'EOF'
[
  {
    "name": "run_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "project_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "asset_type",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "resource_name",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "missing_labels",
    "type": "JSON",
    "mode": "REQUIRED"
  },
  {
    "name": "planned_labels",
    "type": "JSON",
    "mode": "REQUIRED"
  },
  {
    "name": "planned_tags",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "status",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "created_at",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  }
]
EOF

# =====================================================================
# TABLE 4: remediation_execution
# =====================================================================
create_table "remediation_execution" <<'EOF'
[
  {
    "name": "execution_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "run_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "project_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "asset_type",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "resource_name",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "managed_labels",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "status",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "error_message",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "executed_at",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  },
  {
    "name": "execution_mode",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "service_name",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "method_name",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "duration_ms",
    "type": "INT64",
    "mode": "NULLABLE"
  }
]
EOF

echo "All BigQuery tables created successfully in region ${LOCATION}!"

```Create and edit the file:

```Bash
vi create-bq-tables.sh
(Paste the script contents, then save and exit using ESC, then type :wq, Hit Enter)

```Make the file executable:

```Bash
chmod +x create-bq-tables.sh
Run the script:

```Bash
./create-bq-tables.sh



# Step 3 - Configure Governance Registry

The Governance Registry defines the expected metadata for each application.

Repository structure.

```
registry/

    payments.yaml

    platform.yaml

    analytics.yaml

    customer360.yaml
```

Each file represents one application.

Example.

```yaml
schemaVersion: v1

product: payments

team: cloud-platform

owner: john.doe

budgetOwner: finance

organization: example

department: engineering

costCenter: FIN001

bindings:

- cloud: gcp
  projectId: payments-prod
  region: europe-west2
  environment: prod
  businessCriticality: high
```

Validate.

```bash
python validation/validate_registry.py
```

Expected.

```
Validation Passed
```

---

# Step 4 - Create Pub/Sub

Create the event topic.

```bash
gcloud pubsub topics create metadata-governance-events
```

Create the subscription.

```bash
gcloud pubsub subscriptions create metadata-governance-sub \
--topic=metadata-governance-events
```

Verify.

```bash
gcloud pubsub topics list
```

```bash
gcloud pubsub subscriptions list
```

---

# Step 5 - Configure Logging Sink

Create the Logging Sink.

```bash
gcloud logging sinks create metadata-governance-sink \
pubsub.googleapis.com/projects/$PROJECT_ID/topics/metadata-governance-events \
--log-filter='logName:"cloudaudit.googleapis.com"'
```

Verify.

```bash
gcloud logging sinks list
```

---

# Step 6 - Grant Logging Publisher Permissions

Retrieve the writer identity.

```bash
gcloud logging sinks describe metadata-governance-sink
```

Grant Pub/Sub Publisher.

```bash
gcloud pubsub topics add-iam-policy-binding metadata-governance-events \
--member="serviceAccount:LOGGING_WRITER_IDENTITY" \
--role="roles/pubsub.publisher"
```

---

# Step 7 - Create Eventarc Trigger

Cloud Run must already exist before creating the trigger.

```bash
gcloud eventarc triggers create metadata-governance-trigger \
--location=$REGION \
--destination-run-service=metadata-governance \
--destination-run-region=$REGION \
--transport-topic=metadata-governance-events
```

Verify.

```bash
gcloud eventarc triggers list
```

Expected.

```
ACTIVE
```

---

# Step 8 - Execute First Brownfield Scan

Retrieve an Identity Token.

```bash
TOKEN=$(gcloud auth print-identity-token)
```

Execute Brownfield.

```bash
curl \
-H "Authorization: Bearer $TOKEN" \
"https://YOUR_CLOUD_RUN_URL/brownfield?project=$PROJECT_ID"
```

Expected.

- Resources discovered
- Compliance evaluated
- Remediation plan generated
- Reporting tables populated

---

# Step 9 - Verify BigQuery Reporting

Verify inventory.

```sql
SELECT COUNT(*) FROM metadata_governance_dataset.resource_snapshot;
```

Verify compliance.

```sql
SELECT COUNT(*) FROM metadata_governance_dataset.compliance_snapshot;
```

Verify remediation plan.

```sql
SELECT COUNT(*) FROM metadata_governance_dataset.remediation_plan;
```

Verify execution history.

```sql
SELECT COUNT(*) FROM metadata_governance_dataset.remediation_execution;
```

Each table should contain records.

---

# Step 10 - Validate Greenfield Governance

Create a supported resource.

Example.

```bash
gcloud compute instances create governance-test-vm \
--project=$PROJECT_ID \
--zone=europe-west2-a \
--machine-type=e2-micro \
--image-family=debian-12 \
--image-project=debian-cloud
```

Monitor Cloud Run logs.

```bash
gcloud beta run services logs tail metadata-governance \
--region=$REGION
```

Expected processing flow.

```
Audit Event Received

↓

Classification Completed

↓

Registry Match

↓

Compliance Evaluated

↓

Remediation Executed

↓

Reporting Updated
```

---

# Step 11 - Validate Dashboard

Open.

```
https://YOUR_CLOUD_RUN_URL
```

Verify.

## Executive Summary

- Total Resources
- Supported Resources
- Compliance Percentage
- Projects

## Brownfield

- Planned
- Completed
- Remaining
- Failed
- Success Rate

## Greenfield

- Events
- Remediated
- Failed
- Average Processing Time

## Projects

- Organization View
- Project Filter

## Resource Types

- Compliance
- Progress Bars

## Recent Runs

- Latest Brownfield Executions

## Top Non-Compliant Resources

- Missing Labels
- Incorrect Labels

---

# Platform Validation Checklist

| Validation | Status |
|------------|--------|
| BigQuery Dataset Created | ☐ |
| Reporting Tables Created | ☐ |
| Registry Validated | ☐ |
| Pub/Sub Created | ☐ |
| Logging Sink Created | ☐ |
| Logging Publisher Granted | ☐ |
| Eventarc Trigger Active | ☐ |
| Brownfield Successful | ☐ |
| Greenfield Successful | ☐ |
| Dashboard Operational | ☐ |

---

# Deployment Complete

The Enterprise Metadata Governance Platform is now fully operational.

The platform continuously:

- Discovers Google Cloud resources.
- Evaluates metadata compliance.
- Automatically remediates supported resources.
- Processes newly created resources in real time.
- Stores governance history in BigQuery.
- Provides executive dashboards for organization and project governance.
