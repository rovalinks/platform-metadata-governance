resource "google_cloud_run_v2_service" "this" {

  name     = var.service_name
  project  = var.project_id
  location = var.region

  ingress = "INGRESS_TRAFFIC_ALL"

  deletion_protection = false

  template {

    service_account = var.service_account_email

    containers {

      image = var.image

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "REGISTRY_BUCKET"
        value = var.registry_bucket
      }

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }
}