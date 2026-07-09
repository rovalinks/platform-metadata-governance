resource "google_service_account" "scheduler" {
  count = var.enabled ? 1 : 0

  account_id   = "metadata-governance-scheduler"
  display_name = "Metadata Governance Scheduler"
}

resource "google_cloud_run_service_iam_member" "scheduler_invoker" {
  count = var.enabled ? 1 : 0

  project  = var.project_id
  location = var.region
  service  = var.cloud_run_service

  role = "roles/run.invoker"

  member = "serviceAccount:${google_service_account.scheduler[0].email}"
}

resource "google_cloud_scheduler_job" "brownfield_nightly" {
  count = var.enabled ? 1 : 0

  name        = "metadata-governance-nightly"
  description = "Nightly Brownfield Governance Scan"

  project = var.project_id
  region  = var.region

  schedule  = var.schedule
  time_zone = var.time_zone

  http_target {

    uri = "${var.cloud_run_url}/brownfield"

    http_method = "GET"

    oidc_token {
      service_account_email = google_service_account.scheduler[0].email
    }
  }

  depends_on = [
    google_cloud_run_service_iam_member.scheduler_invoker
  ]
}