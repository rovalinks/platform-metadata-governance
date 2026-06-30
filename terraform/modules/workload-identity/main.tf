resource "google_iam_workload_identity_pool" "github" {

  project = data.google_project.current.number

  workload_identity_pool_id = var.workload_identity.pool_id

  display_name = "GitHub Actions Pool"

  description = "OIDC identities from GitHub Actions"

  disabled = false
}

resource "google_iam_workload_identity_pool_provider" "github" {

  project = data.google_project.current.number

  workload_identity_pool_id = google_iam_workload_identity_pool.github.workload_identity_pool_id

  workload_identity_pool_provider_id = var.workload_identity.provider_id

  display_name = "GitHub Provider"

  description = "GitHub Actions OIDC Provider"

  attribute_mapping = {
    "google.subject"             = "assertion.sub"
    "attribute.actor"            = "assertion.actor"
    "attribute.repository"       = "assertion.repository"
    "attribute.repository_owner" = "assertion.repository_owner"
  }

  attribute_condition = "assertion.repository == '${var.workload_identity.github_owner}/${var.workload_identity.github_repository}'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account_iam_member" "github_actions" {

  service_account_id = var.github_service_account

  role = "roles/iam.workloadIdentityUser"

  member = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.workload_identity.github_owner}/${var.workload_identity.github_repository}"
}

data "google_project" "current" {
  project_id = var.project_id
}