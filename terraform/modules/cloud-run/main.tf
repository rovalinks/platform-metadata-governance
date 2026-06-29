resource "google_cloud_run_v2_service" "this" {
  name     = var.service_name
  project  = var.project_id
  location = var.region

  # Set ingress to allow all traffic
  ingress = "INGRESS_TRAFFIC_ALL"

  # Enable deletion protection to prevent accidental removal
  deletion_protection = true

  template {
    service_account = var.service_account_email

    containers {
      image = var.image

      ports {
        container_port = 8080
      }

      # Add resource limits for CPU and Memory
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }
}