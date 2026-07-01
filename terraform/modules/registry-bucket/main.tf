resource "google_storage_bucket" "registry" {

  project = var.project_id

  name = var.bucket_name

  location = var.region

  storage_class = "STANDARD"

  uniform_bucket_level_access = true

  public_access_prevention = "enforced"

  versioning {

    enabled = true

  }

  lifecycle_rule {

    condition {

      age = 90

    }

    action {

      type = "Delete"

    }

  }

}