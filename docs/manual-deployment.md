# Manual Deployment Guide (Without Terraform)

# Purpose

This document describes how to manually deploy the Enterprise Metadata Governance Platform into Google Cloud without using Terraform.

The guide is intended for:

- Cloud Platform Engineers
- Google Cloud Administrators
- Platform Operations Teams
- Support Engineers
- Demonstration Environments
- Proof of Concepts

Every deployment step includes:

- Purpose
- Commands
- Expected Results
- Validation
- Common Issues

Although the platform can be deployed using Terraform, understanding the manual deployment process helps with troubleshooting, platform onboarding, and operational support.

---

# Deployment Overview

The deployment consists of the following phases.

```
Project Setup
        │
        ▼
Enable APIs
        │
        ▼
Create Service Accounts
        │
        ▼
Configure IAM
        │
        ▼
Create Artifact Registry
        │
        ▼
Build Container
        │
        ▼
Deploy Cloud Run
        │
        ▼
Create BigQuery
        │
        ▼
Configure Pub/Sub
        │
        ▼
Configure Eventarc
        │
        ▼
Configure Logging
        │
        ▼
Configure Governance Registry
        │
        ▼
Brownfield Validation
        │
        ▼
Greenfield Validation
        │
        ▼
Dashboard Validation
```

---

# Prerequisites

Before beginning deployment ensure the following software is installed.

| Component | Recommended Version |
|------------|--------------------|
| Google Cloud SDK | Latest |
| Terraform | Latest (optional) |
| Python | 3.12+ |
| Git | Latest |
| Docker | Latest |

Verify installations.

```bash
gcloud version
```

```bash
python --version
```

```bash
docker --version
```

```bash
git --version
```

Expected output should display the installed versions without errors.

---

# Required Google Cloud Permissions

The deploying user should have sufficient permissions to create Google Cloud infrastructure.

Typical deployment permissions include:

- Organization Administrator (or delegated equivalent)
- Project Owner
- Billing Administrator
- IAM Administrator
- Service Usage Administrator

Runtime permissions for the application are documented separately in:

```
docs/iam-permissions.md
```

---

# Step 1 - Create or Select a Google Cloud Project

## Purpose

Create a dedicated project for the Metadata Governance Platform or select an existing project.

Example project:

```
platform-metadata-demo
```

Create a project.

```bash
gcloud projects create platform-metadata-demo
```

Set the active project.

```bash
gcloud config set project platform-metadata-demo
```

Verify.

```bash
gcloud config get-value project
```

Expected output.

```
platform-metadata-demo
```

---

# Step 2 - Enable Billing

The project must have billing enabled before resources can be created.

List billing accounts.

```bash
gcloud billing accounts list
```

Link a billing account.

```bash
gcloud billing projects link platform-metadata-demo \
    --billing-account=BILLING_ACCOUNT_ID
```

Verify.

```bash
gcloud billing projects describe platform-metadata-demo
```

Expected output.

```
billingEnabled: true
```

---

# Step 3 - Authenticate

Authenticate using your Google account.

```bash
gcloud auth login
```

Configure Application Default Credentials.

```bash
gcloud auth application-default login
```

Verify.

```bash
gcloud auth list
```

Expected output should show the active authenticated account.

---

# Step 4 - Enable Required Google Cloud APIs

## Purpose

The platform depends on several managed Google Cloud services.

Enable all required APIs.

```bash
gcloud services enable \
artifactregistry.googleapis.com \
bigquery.googleapis.com \
cloudasset.googleapis.com \
cloudbuild.googleapis.com \
eventarc.googleapis.com \
iam.googleapis.com \
logging.googleapis.com \
pubsub.googleapis.com \
run.googleapis.com \
secretmanager.googleapis.com \
serviceusage.googleapis.com \
sqladmin.googleapis.com \
storage.googleapis.com \
cloudresourcemanager.googleapis.com
```

This process may take several minutes.

Verify.

```bash
gcloud services list --enabled
```

Expected output should include all enabled services.

If an API is missing, enable it individually.

Example.

```bash
gcloud services enable run.googleapis.com
```

---

# Step 5 - Clone the Repository

Clone the Metadata Governance Platform repository.

```bash
git clone https://github.com/<organization>/platform-metadata-governance.git
```

Navigate into the repository.

```bash
cd platform-metadata-governance
```

Verify.

```bash
dir
```

Expected directories.

```
cloudrun
terraform
registry
docs
```

---

# Step 6 - Create the Cloud Run Service Account

## Purpose

The Cloud Run service executes all Brownfield, Greenfield, reporting, and dashboard workloads.

Create the service account.

```bash
gcloud iam service-accounts create metadata-governance \
    --display-name="Metadata Governance"
```

Verify.

```bash
gcloud iam service-accounts list
```

Expected output.

```
metadata-governance@platform-metadata-demo.iam.gserviceaccount.com
```

---

# Step 7 - Configure IAM

Grant the required runtime permissions to the Cloud Run service account.

Replace the project ID if required.

```bash
PROJECT_ID=platform-metadata-demo

SA=metadata-governance@$PROJECT_ID.iam.gserviceaccount.com
```

Grant BigQuery permissions.

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="roles/bigquery.dataEditor"
```

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="roles/bigquery.jobUser"
```

Grant Cloud Asset permissions.

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="roles/cloudasset.viewer"
```

Grant Logging permissions.

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="roles/logging.viewer"
```

Grant Pub/Sub permissions.

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="roles/pubsub.subscriber"
```

Grant Tag permissions.

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="roles/resourcemanager.tagUser"
```

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="roles/resourcemanager.tagViewer"
```

Grant Compute permissions.

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA" \
    --role="roles/compute.admin"
```

Repeat as required for Storage, Cloud SQL, Secret Manager, Artifact Registry, and Cloud KMS.

The complete permission matrix is available in:

```
docs/iam-permissions.md
```

---

# Step 8 - Create Artifact Registry

## Purpose

Artifact Registry stores the Cloud Run container image.

Create the Docker repository.

```bash
gcloud artifacts repositories create metadata-governance \
    --repository-format=docker \
    --location=europe-west2 \
    --description="Metadata Governance Images"
```

Verify.

```bash
gcloud artifacts repositories list
```

Expected output.

```
metadata-governance
```

---

# Step 9 - Configure Docker Authentication

Configure Docker to authenticate with Artifact Registry.

```bash
gcloud auth configure-docker europe-west2-docker.pkg.dev
```

Expected output.

```
Docker configuration updated.
```

---

# Step 10 - Build the Container Image

## Purpose

Cloud Build packages the application into a container image.

Run the build.

```bash
gcloud builds submit \
    --tag europe-west2-docker.pkg.dev/platform-metadata-demo/metadata-governance/metadata-governance:latest
```

Build duration varies depending on the environment.

Verify.

```bash
gcloud builds list
```

Expected output.

```
STATUS: SUCCESS
```

If the build fails.

Check logs.

```bash
gcloud builds log BUILD_ID
```

Resolve any reported issues before continuing.

---

# Step 11 - Verify the Image

List stored images.

```bash
gcloud artifacts docker images list \
europe-west2-docker.pkg.dev/platform-metadata-demo/metadata-governance
```

Expected output.

```
metadata-governance
latest
```

---

# Step 12 - Prepare Cloud Run Deployment

Before deployment gather the following information.

| Setting | Example |
|----------|----------|
| Region | europe-west2 |
| Service Name | metadata-governance |
| Container Image | Artifact Registry Image |
| Service Account | metadata-governance |
| Authentication | IAM |

The next section will deploy Cloud Run, configure environment variables, and connect the application to BigQuery, Pub/Sub, Eventarc, and the Governance Registry.

# Step 13 - Create the BigQuery Dataset

## Purpose

The Enterprise Metadata Governance Platform stores all governance data in BigQuery.

The reporting dataset contains:

- Resource inventory
- Compliance snapshots
- Remediation plans
- Execution history

Create the dataset.

```bash
bq mk \
--location=europe-west2 \
metadata_governance_dataset
```

Verify.

```bash
bq ls
```

Expected output.

```
metadata_governance_dataset
```

If the dataset already exists.

```
Already Exists
```

This can be ignored.

---

# Step 14 - Create Reporting Tables

The platform uses four reporting tables.

| Table | Purpose |
|--------|---------|
| resource_snapshot | Current resource inventory |
| compliance_snapshot | Compliance evaluation results |
| remediation_plan | Planned remediation actions |
| remediation_execution | Remediation execution history |

These tables can be created manually using BigQuery DDL or by applying the provided schemas from the repository.

Verify.

```bash
bq ls metadata_governance_dataset
```

Expected output.

```
resource_snapshot

compliance_snapshot

remediation_plan

remediation_execution
```

---

# Step 15 - Deploy Cloud Run

## Purpose

Cloud Run hosts the Enterprise Metadata Governance Platform.

Deploy the application.

```bash
gcloud run deploy metadata-governance \
    --image=europe-west2-docker.pkg.dev/platform-metadata-demo/metadata-governance/metadata-governance:latest \
    --region=europe-west2 \
    --service-account=metadata-governance@platform-metadata-demo.iam.gserviceaccount.com \
    --allow-unauthenticated=false
```

Cloud Run returns a service URL.

Example.

```
https://metadata-governance-xxxxxxxx.europe-west2.run.app
```

Record this URL.

It will be used throughout the remainder of the deployment.

---

# Step 16 - Configure Environment Variables

The application requires several environment variables.

Update the Cloud Run service.

```bash
gcloud run services update metadata-governance \
    --region=europe-west2 \
    --update-env-vars \
BIGQUERY_DATASET=metadata_governance_dataset,\
REGISTRY_PATH=registry,\
LOG_LEVEL=INFO
```

Verify.

```bash
gcloud run services describe metadata-governance \
--region=europe-west2
```

Check that all environment variables are present.

---

# Step 17 - Validate Cloud Run

Retrieve an Identity Token.

```bash
TOKEN=$(gcloud auth print-identity-token)
```

Health Check.

```bash
curl \
-H "Authorization: Bearer $TOKEN" \
https://YOUR_CLOUD_RUN_URL/health
```

Expected response.

```json
{
    "status":"healthy"
}
```

Verify the dashboard.

```bash
curl \
-H "Authorization: Bearer $TOKEN" \
https://YOUR_CLOUD_RUN_URL/
```

Expected output.

```
Enterprise Metadata Governance Platform
```

---

# Step 18 - Create Pub/Sub Topic

## Purpose

Pub/Sub transports Audit Log events to Eventarc.

Create the topic.

```bash
gcloud pubsub topics create metadata-governance-events
```

Verify.

```bash
gcloud pubsub topics list
```

Expected output.

```
metadata-governance-events
```

---

# Step 19 - Create Pub/Sub Subscription

Create the subscription.

```bash
gcloud pubsub subscriptions create metadata-governance-sub \
    --topic=metadata-governance-events
```

Verify.

```bash
gcloud pubsub subscriptions list
```

Expected output.

```
metadata-governance-sub
```

---

# Step 20 - Configure Organization Logging Sink

## Purpose

The Logging Sink exports Cloud Audit Logs into Pub/Sub.

Create the sink.

```bash
gcloud logging sinks create metadata-governance-sink \
pubsub.googleapis.com/projects/platform-metadata-demo/topics/metadata-governance-events \
--organization=ORGANIZATION_ID \
--log-filter='logName:"cloudaudit.googleapis.com"'
```

Alternatively, create a project-level sink if organization-level permissions are not available.

Verify.

```bash
gcloud logging sinks list
```

Expected output.

```
metadata-governance-sink
```

---

# Step 21 - Grant Logging Sink Permissions

Retrieve the Logging Sink writer identity.

```bash
gcloud logging sinks describe metadata-governance-sink
```

Example.

```
serviceAccount:p123456789@gcp-sa-logging.iam.gserviceaccount.com
```

Grant Pub/Sub Publisher.

```bash
gcloud pubsub topics add-iam-policy-binding metadata-governance-events \
--member="serviceAccount:LOGGING_SERVICE_ACCOUNT" \
--role="roles/pubsub.publisher"
```

Verify.

```bash
gcloud pubsub topics get-iam-policy metadata-governance-events
```

---

# Step 22 - Create Eventarc Trigger

## Purpose

Eventarc delivers Pub/Sub events to Cloud Run.

Create the trigger.

```bash
gcloud eventarc triggers create metadata-governance-trigger \
    --location=europe-west2 \
    --destination-run-service=metadata-governance \
    --destination-run-region=europe-west2 \
    --transport-topic=metadata-governance-events
```

Verify.

```bash
gcloud eventarc triggers list
```

Expected output.

```
metadata-governance-trigger
```

Describe the trigger.

```bash
gcloud eventarc triggers describe metadata-governance-trigger \
--location=europe-west2
```

Expected state.

```
ACTIVE
```

---

# Step 23 - Configure the Governance Registry

The Governance Registry defines the expected metadata for each application.

Each registry file must contain:

- Product
- Team
- Owner
- Budget Owner
- Organization
- Department
- Cost Center

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
  projectId: payments-dev
  region: europe-west2
  environment: dev
  businessCriticality: medium
```

Validate the registry.

```bash
python validation/validate_registry.py
```

Expected output.

```
Validation Passed
```

---

# Step 24 - Configure Resource Manager Tags

If using Resource Manager Tags.

Create Tag Keys.

Example.

```
environment
```

Create Tag Values.

```
dev

test

uat

prod
```

Verify.

```bash
gcloud resource-manager tags keys list
```

Verify values.

```bash
gcloud resource-manager tags values list \
--parent=TAG_KEY_ID
```

---

# Step 25 - Verify Platform Deployment

Confirm the following resources exist.

Cloud Run.

```bash
gcloud run services list
```

Artifact Registry.

```bash
gcloud artifacts repositories list
```

BigQuery.

```bash
bq ls
```

Pub/Sub.

```bash
gcloud pubsub topics list
```

Eventarc.

```bash
gcloud eventarc triggers list
```

Logging.

```bash
gcloud logging sinks list
```

If every component exists, the platform infrastructure has been successfully deployed.

The final section covers Brownfield validation, Greenfield validation, Dashboard validation, operational checks, and post-deployment verification.

# Step 26 - Validate Brownfield Governance

## Purpose

Brownfield governance discovers existing Google Cloud resources, evaluates compliance, generates remediation plans, and executes metadata remediation.

Run a Brownfield scan.

```bash
TOKEN=$(gcloud auth print-identity-token)

curl \
-H "Authorization: Bearer $TOKEN" \
"https://YOUR_CLOUD_RUN_URL/brownfield?project=platform-metadata-demo"
```

Example response.

```json
{
    "project":"platform-metadata-demo",
    "run_id":"761c615e-e4bf-426a-ae3a-b4e4d60641be",
    "status":"COMPLETED",
    "discovered":79604,
    "evaluated":2567,
    "planned":520,
    "successful":420,
    "failed":0
}
```

### Validation

Confirm:

- Resources were discovered.
- Supported resources were evaluated.
- Compliance results were generated.
- A remediation plan was created.
- Execution history was written to BigQuery.

---

# Step 27 - Validate Greenfield Governance

## Purpose

Greenfield governance automatically evaluates newly created resources using Google Cloud Audit Logs.

Create a supported resource.

Example:

```bash
gcloud compute instances create governance-demo-vm \
    --project=platform-metadata-demo \
    --zone=europe-west2-a \
    --machine-type=e2-medium \
    --image-family=debian-12 \
    --image-project=debian-cloud
```

The following workflow should occur automatically.

```
Compute Engine

↓

Cloud Audit Logs

↓

Logging Sink

↓

Pub/Sub

↓

Eventarc

↓

Cloud Run

↓

Classification

↓

Compliance

↓

Remediation

↓

BigQuery
```

---

# Step 28 - Verify Greenfield Processing

Monitor Cloud Run logs.

```bash
gcloud beta run services logs tail metadata-governance \
    --region=europe-west2
```

Expected log sequence.

```
Audit Log received

↓

Classification completed

↓

Resource resolved

↓

Compliance evaluated

↓

Remediation executed

↓

Execution persisted
```

If any stage fails, refer to:

```
docs/troubleshooting.md
```

---

# Step 29 - Verify BigQuery Reporting

Open BigQuery.

Verify the reporting dataset.

```bash
bq ls metadata_governance_dataset
```

Expected tables.

```
resource_snapshot

compliance_snapshot

remediation_plan

remediation_execution
```

Verify snapshots.

```sql
SELECT COUNT(*)
FROM metadata_governance_dataset.resource_snapshot;
```

Verify compliance.

```sql
SELECT COUNT(*)
FROM metadata_governance_dataset.compliance_snapshot;
```

Verify remediation plans.

```sql
SELECT COUNT(*)
FROM metadata_governance_dataset.remediation_plan;
```

Verify execution history.

```sql
SELECT COUNT(*)
FROM metadata_governance_dataset.remediation_execution;
```

Each query should return records after Brownfield or Greenfield processing.

---

# Step 30 - Validate the Executive Dashboard

Open the dashboard.

```
https://YOUR_CLOUD_RUN_URL/
```

Verify the following sections.

## Executive Summary

Confirm:

- Total Resources
- Supported Resources
- Compliance Percentage
- Projects

---

## Brownfield

Confirm:

- Planned
- Completed
- Remaining
- Failed
- Success Rate

---

## Greenfield

Confirm:

- Total Events
- Remediated
- Already Compliant
- Failed
- Average Processing Time

---

## Projects

Verify:

- Organization scope lists all onboarded projects.
- Project scope filters correctly.
- Project metrics match BigQuery.

---

## Resource Types

Verify:

- Compliance percentages
- Resource totals
- Progress indicators

---

## Recent Remediation Runs

Verify:

- Run ID
- Planned
- Completed
- Failed
- Remaining
- Success Rate

---

## Top Non-Compliant Resources

Verify:

- Resource Name
- Resource Type
- Missing Metadata
- Incorrect Metadata

---

# Step 31 - Execute End-to-End Validation

Complete the following checklist.

| Validation | Status |
|------------|--------|
| APIs Enabled | ☐ |
| Cloud Run Healthy | ☐ |
| Artifact Registry Available | ☐ |
| BigQuery Dataset Created | ☐ |
| Reporting Tables Created | ☐ |
| Pub/Sub Configured | ☐ |
| Eventarc Trigger Active | ☐ |
| Logging Sink Active | ☐ |
| Governance Registry Loaded | ☐ |
| Brownfield Successful | ☐ |
| Greenfield Successful | ☐ |
| Dashboard Operational | ☐ |

All items should be complete before handing the platform to users.

---

# Step 32 - Operational Validation

Run the following commands.

Cloud Run

```bash
gcloud run services list
```

Eventarc

```bash
gcloud eventarc triggers list
```

Pub/Sub

```bash
gcloud pubsub topics list
```

BigQuery

```bash
bq ls
```

Artifact Registry

```bash
gcloud artifacts repositories list
```

IAM

```bash
gcloud projects get-iam-policy platform-metadata-demo
```

Cloud Run Logs

```bash
gcloud beta run services logs tail metadata-governance \
    --region=europe-west2
```

All commands should complete without errors.

---

# Step 33 - Post-Deployment Recommendations

After deployment, perform the following operational tasks.

- Protect the main branch using Pull Requests.
- Enable Cloud Run Monitoring and Alerting.
- Enable BigQuery cost monitoring.
- Review IAM permissions regularly.
- Schedule Brownfield scans.
- Keep the Governance Registry current.
- Monitor failed remediations.
- Review dashboard KPIs regularly.
- Maintain documentation alongside code changes.

---

# Deployment Complete

The Enterprise Metadata Governance Platform has now been deployed and validated.

The platform is capable of:

- Discovering existing Google Cloud resources.
- Evaluating metadata compliance.
- Planning and executing metadata remediation.
- Automatically governing newly created resources.
- Producing centralized governance reporting.
- Providing organization-level and project-level executive dashboards.

Refer to the remaining documentation for ongoing operations and maintenance:

- `docs/architecture.md`
- `docs/brownfield.md`
- `docs/greenfield.md`
- `docs/dashboard.md`
- `docs/operations.md`
- `docs/troubleshooting.md`
- `docs/iam-permissions.md`