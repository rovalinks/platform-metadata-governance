module "artifact_registry" {

  source = "./modules/artifact-registry"

  project_id = var.project_id

  region = var.region

  repository_id = var.artifact_registry_repository

  description = var.artifact_registry_description

}

module "service_accounts" {
  source = "./modules/service-accounts"

  project_id       = var.project_id
  service_accounts = var.service_accounts
}

module "iam" {
  source = "./modules/iam"

  project_id = var.project_id

  service_account_emails = module.service_accounts.emails

  service_account_roles = var.service_account_roles
}

module "cloud_run" {

  count = var.deploy_cloud_run ? 1 : 0

  source = "./modules/cloud-run"

  project_id = var.project_id

  region = var.region

  service_name = var.cloud_run.service_name

  image = var.cloud_run.image

  service_account_email = module.service_accounts.emails["governance"]
}

module "workload_identity" {
  source = "./modules/workload-identity"

  project_id = var.project_id

  github_service_account = module.service_accounts.names["github"]

  workload_identity = var.workload_identity
}

