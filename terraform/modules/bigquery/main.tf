resource "google_bigquery_dataset" "metadata" {

  project = var.project_id

  dataset_id = var.dataset_id

  location = var.region

  description = "Metadata Governance snapshots"

  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "resource_inventory" {

  project = var.project_id

  dataset_id = google_bigquery_dataset.metadata.dataset_id

  table_id = "resource_inventory"

  deletion_protection = false

  schema = file("${path.module}/schemas/resource_inventory.json")
}

resource "google_bigquery_table" "compliance_results" {

  project = var.project_id

  dataset_id = google_bigquery_dataset.metadata.dataset_id

  table_id = "compliance_results"

  deletion_protection = false

  schema = file("${path.module}/schemas/compliance_results.json")
}