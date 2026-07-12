output "sink_name" {
  value = google_logging_organization_sink.greenfield.name
}

output "writer_identity" {
  value = google_logging_organization_sink.greenfield.writer_identity
}