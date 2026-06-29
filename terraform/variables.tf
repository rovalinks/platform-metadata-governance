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

variable "service_account_roles" {
  description = "IAM roles assigned to service accounts"

  type = map(list(string))
}

variable "cloud_run" {
  type = object({
    service_name = string
    image        = string
  })
}

variable "workload_identity" {
  description = "GitHub Workload Identity Federation configuration"

  type = object({
    pool_id            = string
    provider_id        = string
    github_owner       = string
    github_repository  = string
  })
}