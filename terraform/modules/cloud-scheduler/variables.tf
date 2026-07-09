variable "enabled" {
  description = "Enable Cloud Scheduler deployment."
  type        = bool
  default     = true
}

variable "project_id" {
  description = "GCP Project ID."
  type        = string
}

variable "region" {
  description = "Scheduler region."
  type        = string
}

variable "cloud_run_service" {
  description = "Cloud Run service name."
  type        = string
}

variable "cloud_run_url" {
  description = "Cloud Run service URL."
  type        = string
}

variable "schedule" {
  description = "Cron schedule."
  type        = string
  default     = "0 2 * * *"
}

variable "time_zone" {
  description = "Scheduler timezone."
  type        = string
  default     = "Europe/London"
}