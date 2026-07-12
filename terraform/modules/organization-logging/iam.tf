resource "google_pubsub_topic_iam_member" "organization_sink_publisher" {
  project = var.project_id
  topic   = var.topic_name

  role   = "roles/pubsub.publisher"
  member = google_logging_organization_sink.greenfield.writer_identity
}