resource "google_bigquery_dataset" "metadata" {

  project = var.project_id

  dataset_id = var.dataset_id

  location = var.region

  description = "Metadata Governance snapshots"

  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "resource_snapshot" {

  project = var.project_id

  dataset_id = google_bigquery_dataset.metadata.dataset_id

  table_id = "resource_snapshot"

  deletion_protection = false

  schema = file("${path.module}/schemas/resource_inventory.json")
}

resource "google_bigquery_table" "compliance_snapshot" {

  project = var.project_id

  dataset_id = google_bigquery_dataset.metadata.dataset_id

  table_id = "compliance_snapshot"

  deletion_protection = false

  schema = file("${path.module}/schemas/compliance_results.json")
}

resource "google_bigquery_table" "remediation_plan" {

  project = var.project_id

  dataset_id = google_bigquery_dataset.metadata.dataset_id

  table_id = "remediation_plan"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/remediation_plan.json"
  )
}

resource "google_bigquery_table" "remediation_execution" {

  project = var.project_id

  dataset_id = google_bigquery_dataset.metadata.dataset_id

  table_id = "remediation_execution"

  deletion_protection = false

  schema = file(
    "${path.module}/schemas/remediation_execution.json"
  )
}

resource "google_bigquery_table" "label_ownership" {

  project             = var.project_id
  dataset_id          = google_bigquery_dataset.metadata.dataset_id
  table_id            = "label_ownership"
  deletion_protection = false

  schema = file(
    "${path.module}/schemas/label_ownership.json"
  )

  clustering = [
    "resource_name"
  ]
}