variable "project_id" {
  description = "Google Cloud project ID"

  type = string
}

variable "region" {
  description = "Default deployment region"

  type = string
}

variable "artifact_registry_repository" {
  description = "Artifact Registry repository name"

  type = string
}

variable "artifact_registry_description" {
  description = "Artifact Registry description"

  type = string
}

variable "service_accounts" {
  description = "Service accounts used by the platform"

  type = map(object({
    account_id   = string
    display_name = string
    description  = string
  }))
}

variable "cloud_run_service_name" {
  description = "Cloud Run service name"

  type = string
}

variable "container_image" {
  description = "Container image URI"

  type = string
}