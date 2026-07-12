resource "google_logging_organization_sink" "greenfield" {
  name             = "metadata-governance-greenfield"
  org_id           = var.organization_id
  include_children = true
  destination      = "pubsub.googleapis.com/projects/${var.project_id}/topics/${var.topic_name}"
  filter           = local.greenfield_filter
}