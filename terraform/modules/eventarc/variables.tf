variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Region hosting the Cloud Run service"
  type        = string
}

variable "trigger_name" {
  description = "Eventarc trigger name"
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