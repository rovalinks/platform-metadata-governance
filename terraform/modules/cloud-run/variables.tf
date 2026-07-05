variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Deployment region"
  type        = string
}

variable "service_name" {
  description = "Cloud Run service name"
  type        = string
}

variable "image" {
  description = "Container image URI"
  type        = string
}

variable "service_account_email" {
  description = "Runtime service account"
  type        = string
}

variable "registry_bucket" {
  description = "Registry Cloud Storage bucket"
  type        = string
}

variable "registry_cache_ttl" {
  type    = number
  default = 300
}

variable "excluded_buckets" {
  type = list(string)
}

variable "dry_run" {
  type    = bool
  default = false
}

variable "log_level" {
  type    = string
  default = "INFO"
}

variable "task_queue" {
  type = string
}

variable "cloud_run_url" {
  type    = string
  default = ""
}