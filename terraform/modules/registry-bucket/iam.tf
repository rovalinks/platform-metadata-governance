resource "google_storage_bucket_iam_member" "github_registry_writer" {

  bucket = google_storage_bucket.registry.name

  role = "roles/storage.objectAdmin"

  member = "serviceAccount:${var.github_service_account}"

}