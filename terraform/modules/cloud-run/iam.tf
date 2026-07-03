resource "google_cloud_run_v2_service_iam_member" "eventarc_invoker" {

  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.this.name

  role = "roles/run.invoker"

  member = "serviceAccount:${var.service_account_email}"

}