resource "google_cloud_tasks_queue" "remediation" {

  project  = var.project_id
  location = var.region

  name = var.queue_name

  rate_limits {

    max_dispatches_per_second = 20

    max_concurrent_dispatches = 20
  }

  retry_config {

    max_attempts = 5

    min_backoff = "5s"

    max_backoff = "300s"

    max_doublings = 5
  }

  stackdriver_logging_config {

    sampling_ratio = 1.0
  }
}
