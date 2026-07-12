resource "google_pubsub_topic" "governance" {
  project                    = var.project_id
  name                       = var.topic_name
  message_retention_duration = "604800s"

}

resource "google_pubsub_subscription" "governance" {
  project                    = var.project_id
  name                       = var.subscription_name
  topic                      = google_pubsub_topic.governance.id
  ack_deadline_seconds       = 30
  message_retention_duration = "604800s"
  retry_policy {
    minimum_backoff = "5s"
    maximum_backoff = "60s"
  }

  push_config {
    push_endpoint = "${var.cloud_run_url}/events/pubsub"
    oidc_token {
      service_account_email = var.push_service_account
    }

  }

}