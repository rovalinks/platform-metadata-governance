resource "google_cloud_run_v2_service" "this" {

  name     = var.service_name
  project  = var.project_id
  location = var.region

  ingress = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {

    service_account = var.service_account_email

    containers {

      image = var.image

      ports {
        container_port = 8080
      }

    }

  }

}