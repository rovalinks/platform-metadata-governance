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