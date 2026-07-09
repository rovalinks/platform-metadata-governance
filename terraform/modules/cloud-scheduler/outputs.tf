output "scheduler_job_name" {
  value = var.enabled ? google_cloud_scheduler_job.brownfield_nightly[0].name : null
}

output "scheduler_service_account" {
  value = var.enabled ? google_service_account.scheduler[0].email : null
}