variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Artifact Registry region"
  type        = string
}

variable "repository_id" {
  description = "Artifact Registry repository name"
  type        = string
}

variable "description" {
  description = "Repository description"
  type        = string
}