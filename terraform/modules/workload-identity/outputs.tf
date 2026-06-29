output "workload_identity_provider" {
  description = "Workload Identity Provider"

  value = google_iam_workload_identity_pool_provider.github.name
}

output "workload_identity_pool" {
  description = "Workload Identity Pool"

  value = google_iam_workload_identity_pool.github.name
}