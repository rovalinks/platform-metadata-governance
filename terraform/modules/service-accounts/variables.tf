variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "service_accounts" {
  description = "Map of service accounts to create or manage"

  type = map(object({
    account_id   = string
    display_name = string
    description  = string
  }))
}