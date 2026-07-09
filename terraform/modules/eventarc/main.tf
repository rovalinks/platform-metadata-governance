resource "google_eventarc_trigger" "this" {

  for_each = {

    for trigger in var.triggers :

    trigger.name => trigger

  }

  name = each.value.name

  project = var.project_id

  location = each.value.location

  matching_criteria {

    attribute = "type"

    value = "google.cloud.audit.log.v1.written"

  }

  matching_criteria {

    attribute = "serviceName"

    value = each.value.service

  }

  matching_criteria {

    attribute = "methodName"

    value = each.value.method

  }

  destination {

    cloud_run_service {

      service = var.cloud_run_service

      region = var.region

    }

  }

  service_account = var.service_account_email

}