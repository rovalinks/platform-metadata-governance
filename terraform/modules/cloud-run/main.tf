resource "google_cloud_run_v2_service" "this" {
  name                = var.service_name
  project             = var.project_id
  location            = var.region
  ingress             = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false

  template {
    service_account = var.service_account_email
    timeout         = "900s"

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

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
      env {
        name  = "EXCLUDED_BUCKETS"
        value = join(",", var.excluded_buckets)
      }
      env {
        name  = "REGISTRY_CACHE_TTL"
        value = tostring(var.registry_cache_ttl)
      }
      env {
        name  = "BIGQUERY_DATASET"
        value = var.bigquery.dataset_id
      }
      env {
        name  = "DRY_RUN"
        value = tostring(var.dry_run)
      }
      env {
        name  = "LOG_LEVEL"
        value = var.log_level
      }

      env {
        name  = "TASK_QUEUE"
        value = var.task_queue
      }

      env {
        name  = "REGION"
        value = var.region
      }

      env {
        name  = "SERVICE_ACCOUNT_EMAIL"
        value = var.service_account_email
      }

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
      }
    }
  }

  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers[0].image
    ]
  }
}

variable "bigquery" {
  description = "BigQuery configuration"

  type = object({
    dataset_id = string
  })
}