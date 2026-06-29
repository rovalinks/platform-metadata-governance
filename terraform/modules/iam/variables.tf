variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "service_account_emails" {
  description = "Map of service account emails"

  type = map(string)
}

variable "service_account_roles" {
  description = "Roles assigned to each service account"

  type = map(list(string))
}