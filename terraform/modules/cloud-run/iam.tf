resource "google_cloud_run_v2_service_iam_member" "eventarc_invoker" {

  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.this.name

  role = "roles/run.invoker"

  member = "serviceAccount:${var.service_account_email}"

}

resource "google_cloud_run_v2_service_iam_member" "developer_invoker" {

  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.this.name

  role = "roles/run.invoker"

  member = "user:rohith555raju@gmail.com"
}


# For a customer deployment, nee to  replace:

# member = "user:rohith555raju@gmail.com"
# with
# member = "domain:customer.com"
# or preferably
# member = "group:platform-engineers@customer.com"