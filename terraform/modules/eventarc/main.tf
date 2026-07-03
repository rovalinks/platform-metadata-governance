resource "google_eventarc_trigger" "this" {

  name     = var.trigger_name
  project  = var.project_id
  location = var.region

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.audit.log.v1.written"
  }

  matching_criteria {
    attribute = "serviceName"
    value     = "compute.googleapis.com"
  }

  matching_criteria {
    attribute = "methodName"
    value     = "v1.compute.instances.insert"
  }

  destination {
    cloud_run_service {
      service = var.cloud_run_service
      region  = var.region
    }
  }

  service_account = var.service_account_email

}