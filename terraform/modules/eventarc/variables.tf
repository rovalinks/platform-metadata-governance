variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Region hosting the Cloud Run service"
  type        = string
}

variable "cloud_run_service" {
  description = "Cloud Run service name"
  type        = string
}

variable "service_account_email" {
  description = "Service account used by Eventarc"
  type        = string
}

variable "triggers" {

  description = "Audit Log triggers"

  type = list(object({

    name = string

    service = string

    method = string

  }))
}