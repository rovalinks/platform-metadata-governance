variable "project_id" {
  type = string
}

variable "github_service_account" {
  type = string
}

variable "workload_identity" {
  type = object({
    pool_id           = string
    provider_id       = string
    github_owner      = string
    github_repository = string
  })
}