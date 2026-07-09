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
    pool_id           = string
    provider_id       = string
    github_owner      = string
    github_repository = string
  })
}

variable "deploy_cloud_run" {
  description = "Deploy Cloud Run service"

  type    = bool
  default = false
}

variable "registry_bucket_name" {

  type = string

}

variable "registry_cache_ttl" {
  description = "Registry cache TTL in seconds"
  type        = number
  default     = 300
}

variable "excluded_buckets" {
  description = "Buckets excluded from enforcement"
  type        = list(string)
  default     = []
}

variable "dry_run" {
  description = "Enable dry-run enforcement"
  type        = bool
  default     = false
}

variable "log_level" {
  description = "Application log level"
  type        = string
  default     = "INFO"
}


variable "bigquery" {
  description = "BigQuery configuration"

  type = object({
    dataset_id = string
  })
}

variable "eventarc" {
  description = "Eventarc configuration"

  type = object({
    triggers = list(object({
      name     = string
      service  = string
      method   = string
      location = string
    }))
  })
}

variable "brownfield_schedule" {
  description = "Nightly Brownfield schedule."
  type        = string
  default     = "0 2 * * *"
}

variable "brownfield_time_zone" {
  description = "Timezone for Brownfield scheduler."
  type        = string
  default     = "Europe/London"
}

variable "enable_cloud_scheduler" {
  description = "Deploy Cloud Scheduler."
  type        = bool
  default     = true
}