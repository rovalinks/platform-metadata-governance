variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "topic_name" {
  type = string
}

variable "subscription_name" {
  type = string
}

variable "cloud_run_url" {
  type = string
}

variable "push_service_account" {
  type = string
}

variable "cloud_run_service_name" {
  description = "Cloud Run service name"
  type        = string
}